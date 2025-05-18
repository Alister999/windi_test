import uuid
from typing import Set

import sqlalchemy
from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.core.ConnectionManager import ConnectionManager
from src.core.database import get_db, GroupRepository
from src.core.utils import get_current_user_ws
from src.models.group import Group
from src.models.message import Message
from src.models.user import User
from src.schemas.messages import MessageCreate
import logging

from src.services.message_service import create_message_now

logger = logging.Logger(__name__)

router = APIRouter()
manager = ConnectionManager()



async def get_group_user_ids(db: AsyncSession, group_id: int) -> Set[int]:
    try:
        result = await db.execute(select(Group).where(Group.id == group_id))
        group = result.scalars().first()
        if not group: #chat:
            logger.error(f"Chat not found: id={group_id}")
            return set()
        user_ids = {user.id for user in group.users} #chat.users}
        logger.info(f"Group {group_id} users: {user_ids}")
        return user_ids
    except Exception as e:
        logger.error(f"Error getting user IDs for chat {group_id}: {str(e)}")
        return set()


@router.websocket("/ws/chat/{group_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        group_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_ws)
):

    logger.info(f"Connecting user (name: {current_user.name}, id: {current_user.id})")

    repo_group = GroupRepository(session=db)
    check_group = await repo_group.get_one_or_none(Group.id == group_id)
    if not check_group:
        logger.error(f"Group is absent: id={group_id}")
        await websocket.send_json({"error": f"Group with id '{group_id}' not found"})
        await websocket.close(code=1008)
        return

    user_ids = await get_group_user_ids(db, group_id)
    if current_user.id not in user_ids:
        logger.error(f"User {current_user.name} (id: {current_user.id}) not in group {group_id}")
        await websocket.send_json({"error": f"User not a member of group {group_id}"})
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, group_id, current_user.id)
    logger.info(f"Group id - {group_id}, username - {current_user.name}")


    try:
        while True:
            try:
                data = await websocket.receive_text()
                logger.error(data)

                new_mess = Message(
                    text=data,
                    chat_id=group_id,
                    sender_id=current_user.id,
                    client_message_id=str(uuid.uuid4())
                )

                formatted_message = MessageCreate.model_validate(new_mess)

                async with async_sessionmaker(db.bind, expire_on_commit=False)() as session:
                    response = await create_message_now(formatted_message, session)

                    broadcast_message = f"{current_user.name}: {response.text}"
                    await manager.broadcast(broadcast_message, group_id, user_ids)

            except sqlalchemy.exc.MissingGreenlet as e:
                logger.error(f"MissingGreenlet error for user {current_user.name}: {str(e)}")
                await websocket.send_json({"error": "Internal database error: async context issue"})
                continue
            except Exception as e:
                logger.error(f"Error processing message from user {current_user.name}: {str(e)}")
                await websocket.send_json({"error": f"Error: {str(e)}"})
                continue

    except Exception as e:
        logger.error(f"WebSocket error for user {current_user.name} in chat {group_id}: {str(e)}")
        await websocket.close(code=1000)

