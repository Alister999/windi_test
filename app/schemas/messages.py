from datetime import datetime

from pydantic import BaseModel

from app.models.message import ReadType


class MessageGroup(BaseModel):
    class Config:
        from_attributes = True


class MessageCreate(MessageGroup):
    text: str
    timestamp: datetime
    is_read: ReadType = ReadType.UNREAD


class MessageResponse(MessageGroup):
    id: int
    text: str
    timestamp: datetime
    is_read: ReadType