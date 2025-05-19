from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from src.models.message import ReadType


class MessageGroup(BaseModel):
    class Config:
        from_attributes = True


class MessageCreate(MessageGroup):
    chat_id: int
    text: str = Field(max_length=200)
    client_message_id: str
    sender_id: Optional[int]


class MessageCreateGroup(MessageGroup):
    group_id: int
    text: str = Field(max_length=200)
    client_message_id: str
    sender_id: Optional[int]


class MessageResponse(MessageGroup):
    id: int
    chat_id: Optional[int]
    group_id: Optional[int]
    sender_id: int
    text: str
    client_message_id: str
    is_read: ReadType = ReadType.UNREAD
    timestamp: datetime


class MessageHistory(MessageGroup):
    chat_id: int
    text: str
    sender_id: int
