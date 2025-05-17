import uuid

import sqlalchemy
from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.core.ConnectionManager import ConnectionManager
from src.core.database import get_db
from src.core.utils import get_current_user_ws
from src.models.message import Message
from src.models.user import User
from src.schemas.messages import MessageCreate
import logging

from src.services.message_service import create_message_now

logger = logging.Logger(__name__)

router = APIRouter()
manager = ConnectionManager()



@router.websocket("/ws/chat/{chat_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_ws)
):
    logger.error(f"Connecting user (name: {current_user.name}, id: {current_user.id})")
    await websocket.accept()
    logger.error(f"chat id - {chat_id}, username - {current_user.name}")
    try:
        while True:
            try:
                data = await websocket.receive_text()
                logger.error(data)

                new_mess = Message(
                    text=data,
                    chat_id=chat_id,
                    sender_id=current_user.id, #int(username),
                    client_message_id=str(uuid.uuid4())
                )

                formatted_message = MessageCreate.model_validate(new_mess)

                async with async_sessionmaker(db.bind, expire_on_commit=False)() as session:
                    await create_message_now(formatted_message, session)

                await websocket.send_text(f"Message {data} is send")

            except sqlalchemy.exc.MissingGreenlet as e:
                logger.error(f"MissingGreenlet error for user {current_user.name}: {str(e)}")
                await websocket.send_json({"error": "Internal database error: async context issue"})
                continue
            except Exception as e:
                logger.error(f"Error processing message from user {current_user.name}: {str(e)}")
                await websocket.send_json({"error": f"Error: {str(e)}"})
                continue

    except Exception as e:
        logger.error(f"WebSocket error for user {current_user.name} in chat {chat_id}: {str(e)}")
        await websocket.close(code=1000)

