from datetime import datetime

from pydantic import BaseModel, Field

from src.models.message import ReadType


class MessageGroup(BaseModel):
    class Config:
        from_attributes = True


class MessageCreate(MessageGroup):
    text: str = Field(max_length=200)
    chat_id: int
    sender_id: int


class MessageResponse(MessageGroup):
    id: int
    text: str
    chat_id: int
    sender_id: int
    timestamp: datetime
    is_read: ReadType = ReadType.UNREAD