from fastapi import WebSocket
from typing import Dict, Set
import logging

logger = logging.getLogger("ConnectionManager")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: int, user_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = {}
        self.active_connections[chat_id][user_id] = websocket
        logger.info(f"User {user_id} connected to chat {chat_id}")

    def disconnect(self, chat_id: int, user_id: int):
        if chat_id in self.active_connections and user_id in self.active_connections[chat_id]:
            del self.active_connections[chat_id][user_id]
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]
            logger.info(f"User {user_id} disconnected from chat {chat_id}")

    async def broadcast(self, message: dict, chat_id: int, user_ids: Set[int]):
        for user_id in user_ids:
            if chat_id in self.active_connections and user_id in self.active_connections[chat_id]:
                try:
                    await self.active_connections[chat_id][user_id].send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id} in chat {chat_id}: {str(e)}")
                    self.disconnect(chat_id, user_id)