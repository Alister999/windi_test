import logging
import uuid
from typing import Set
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.websockets import WebSocket
from src.core.ConnectionManager import ConnectionManager
from src.models.chats import Chat
from src.models.group import Group
from src.models.message import Message
from src.models.user import User
from src.schemas.messages import MessageCreateGroup, MessageCreate
from src.services.message_service import create_message_now


logger = logging.Logger(__name__)


async def get_group_user_ids(db: AsyncSession, group_id: int) -> Set[int]:
    try:
        result = await db.execute(select(Group).where(Group.id == group_id))
        group = result.scalars().first()
        if not group: #chat:
            logger.error(f"Group not found: id={group_id}")
            return set()
        user_ids = {user.id for user in group.users}
        logger.info(f"Group {group_id} users: {user_ids}")
        return user_ids
    except Exception as e:
        logger.error(f"Error getting user IDs for group {group_id}: {str(e)}")
        return set()


async def get_direct_chat_user_ids(db: AsyncSession, chat_id: int) -> Set[int]:
    try:
        result = await db.execute(select(Chat).where(Chat.id == chat_id))
        chat = result.scalars().first()
        if not chat:
            logger.error(f"Direct chat not found: id={chat_id}")
            return set()
        user_ids = {user.id for user in chat.users}
        logger.info(f"Direct chat {chat_id} users: {user_ids}")
        return user_ids
    except Exception as e:
        logger.error(f"Error getting user IDs for direct chat {chat_id}: {str(e)}")
        return set()


async def group_connection(websocket: WebSocket, group_id: int,
                           current_user: User, db: AsyncSession,
                           user_ids: set[int], manager: ConnectionManager):
    try:
        while True:
            try:
                data = await websocket.receive_text()
                logger.error(f'Data - {data}')

                new_mess = Message(
                    text=data,
                    group_id=group_id,
                    sender_id=current_user.id,
                    client_message_id=str(uuid.uuid4())
                )

                formatted_message = MessageCreateGroup.model_validate(new_mess)

                async with async_sessionmaker(db.bind, expire_on_commit=False)() as session:
                    response = await create_message_now(formatted_message, session)

                    broadcast_message = f"{current_user.name}: {response.text}"
                    await manager.broadcast(broadcast_message, group_id, user_ids)

            except sqlalchemy.exc.MissingGreenlet as e:
                logger.error(f"MissingGreenlet error for user {current_user.name}: {str(e)}")
                await websocket.accept()
                await websocket.send_json({"error": "Internal database error: async context issue"})
                continue
            except Exception as e:
                logger.error(f"Error processing message from user {current_user.name}: {str(e)}")
                await websocket.accept()
                await websocket.send_json({"error": f"Error: {str(e)}"})
                continue

    except Exception as e:
        logger.error(f"WebSocket error for user {current_user.name} in group {group_id}: {str(e)}")
        await websocket.close(code=1000)


async def chat_connection(websocket: WebSocket, chat_id: int,
                           current_user: User, db: AsyncSession,
                           user_ids: set[int], manager: ConnectionManager):
    try:
        while True:
            try:
                data = await websocket.receive_text()
                logger.error(f"Received data: {data}")

                new_mess = Message(
                    text=data,
                    chat_id=chat_id,
                    sender_id=current_user.id,
                    client_message_id=str(uuid.uuid4())
                )

                formatted_message = MessageCreate.model_validate(new_mess)

                async with async_sessionmaker(db.bind, expire_on_commit=False)() as session:
                    response = await create_message_now(formatted_message, session)
                    broadcast_message = f"{current_user.name}: {response.text}"
                    await manager.broadcast(broadcast_message, chat_id, user_ids)

            except sqlalchemy.exc.MissingGreenlet as e:
                logger.error(f"MissingGreenlet error for user {current_user.name}: {str(e)}")
                await websocket.accept()
                await websocket.send_json({"error": "Internal database error: async context issue"})
                continue
            except Exception as e:
                logger.error(f"Error processing message from user {current_user.name}: {str(e)}")
                await websocket.accept()
                continue

    except Exception as e:
        logger.error(f"WebSocket error for user {current_user.name} in direct chat {chat_id}: {str(e)}")
        manager.disconnect(chat_id, current_user.id)
        await websocket.close(code=1000)