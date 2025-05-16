from fastapi import APIRouter, WebSocket, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.ConnectionManager import ConnectionManager
from src.core.database import get_db
from src.core.dependencies import SessionDep
from src.core.utils import get_current_user, get_current_user_ws
from src.models.message import Message
from src.models.user import User
from src.models.group import Group
from src.schemas.messages import MessageCreate, MessageResponse
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select
from typing import Set

router = APIRouter()
manager = ConnectionManager()


class MessageRepository(SQLAlchemyAsyncRepository[Message]):
    model_type = Message


class GroupRepository(SQLAlchemyAsyncRepository[Group]):
    model_type = Group


async def get_recipient_ids(db: AsyncSession, chat_id: int, sender_id: int) -> Set[int]:
    group = await db.execute(select(Group).where(Group.id == chat_id))
    group = group.scalars().first()
    if not group:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {user.id for user in group.users if user.id != sender_id}


@router.websocket("/ws/chat/{chat_id}/{user_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: int,
        user_id: int,
        token: str = Query(...),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_ws)
):
    if current_user.id != user_id:
        await websocket.close(code=1008, reason="Unauthorized")
        return

    group_repo = GroupRepository(session=db)
    group = await group_repo.get_one_or_none(Group.id == chat_id)
    if not group or user_id not in {u.id for u in group.users}:
        await websocket.close(code=1008, reason="User not in chat")
        return

    await manager.connect(websocket, chat_id, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "message":
                message_data = MessageCreate(
                    chat_id=chat_id,
                    text=data["text"],
                    client_message_id=data["client_message_id"]
                )

                message_repo = MessageRepository(session=db)
                existing_message = await message_repo.get_one_or_none(
                    Message.client_message_id == message_data.client_message_id
                )
                if existing_message:
                    continue

                message = Message(
                    chat_id=message_data.chat_id,
                    sender_id=user_id,
                    text=message_data.text,
                    client_message_id=message_data.client_message_id
                )

                await message_repo.add(message)
                await db.commit()
                await db.refresh(message)

                response = MessageResponse.model_validate(message)
                broadcast_message = {
                    "type": "message",
                    "message": response.dict()
                }

                recipient_ids = await get_recipient_ids(db, chat_id, user_id)
                await manager.send_message(broadcast_message, chat_id, recipient_ids | {user_id})

            elif message_type == "read":
                message_id = data["message_id"]
                message_repo = MessageRepository(session=db)
                message = await message_repo.get_one_or_none(Message.id == message_id)
                if message and message.chat_id == chat_id and not message.is_read:
                    message.is_read = True
                    await db.commit()
                    await manager.broadcast_read_status(chat_id, message_id, user_id)

    except Exception as e:
        await manager.disconnect(websocket, chat_id, user_id)
        await websocket.close(code=1000)