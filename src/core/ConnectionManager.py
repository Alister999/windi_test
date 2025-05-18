# from fastapi import WebSocket
# from typing import Dict, Set
# from collections import defaultdict
#
#
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: Dict[int, Dict[int, Set[WebSocket]]] = defaultdict(lambda: defaultdict(set))
#
#     async def connect(self, websocket: WebSocket, chat_id: int, user_id: int):
#         await websocket.accept()
#         self.active_connections[chat_id][user_id].add(websocket)
#
#     def disconnect(self, websocket: WebSocket, chat_id: int, user_id: int):
#         self.active_connections[chat_id][user_id].discard(websocket)
#         if not self.active_connections[chat_id][user_id]:
#             del self.active_connections[chat_id][user_id]
#         if not self.active_connections[chat_id]:
#             del self.active_connections[chat_id]
#
#     async def send_message(self, message: dict, chat_id: int, recipient_ids: Set[int]):
#         for user_id in recipient_ids:
#             for websocket in self.active_connections[chat_id].get(user_id, set()):
#                 await websocket.send_json(message)
#
#     async def broadcast_read_status(self, chat_id: int, message_id: int, user_id: int):
#         message = {"type": "read_status", "message_id": message_id, "user_id": user_id}
#         for uid, websockets in self.active_connections[chat_id].items():
#             for websocket in websockets:
#                 await websocket.send_json(message)

# src/core/connection_manager.py
from fastapi import WebSocket
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Храним соединения: {chat_id: {user_id: WebSocket}}
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