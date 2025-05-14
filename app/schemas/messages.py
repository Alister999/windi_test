from datetime import datetime

from pydantic import BaseModel

from app.models.message import ReadType


class MessageGroup(BaseModel):
    class Config:
        from_attributes = True


class MessageCreate(MessageGroup):
    text: str
    chat_id: int
    sender_id: int


class MessageResponse(MessageGroup):
    id: int
    text: str
    chat_id: int
    sender_id: int
    timestamp: datetime
    is_read: ReadType = ReadType.UNREAD