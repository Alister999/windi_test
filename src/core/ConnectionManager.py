from fastapi import WebSocket
from typing import Dict, Set
from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, Set[WebSocket]]] = defaultdict(lambda: defaultdict(set))

    async def connect(self, websocket: WebSocket, chat_id: int, user_id: int):
        await websocket.accept()
        self.active_connections[chat_id][user_id].add(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: int, user_id: int):
        self.active_connections[chat_id][user_id].discard(websocket)
        if not self.active_connections[chat_id][user_id]:
            del self.active_connections[chat_id][user_id]
        if not self.active_connections[chat_id]:
            del self.active_connections[chat_id]

    async def send_message(self, message: dict, chat_id: int, recipient_ids: Set[int]):
        for user_id in recipient_ids:
            for websocket in self.active_connections[chat_id].get(user_id, set()):
                await websocket.send_json(message)

    async def broadcast_read_status(self, chat_id: int, message_id: int, user_id: int):
        message = {"type": "read_status", "message_id": message_id, "user_id": user_id}
        for uid, websockets in self.active_connections[chat_id].items():
            for websocket in websockets:
                await websocket.send_json(message)