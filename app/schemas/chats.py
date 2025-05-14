from pydantic import BaseModel

from app.models.chats import ChatType


class BaseChat(BaseModel):
    class Config:
        from_attributes = True


class ChatCreate(BaseChat):
    name_chat: str
    type: ChatType = ChatType.PERSONAL
    creator_id: int


class ChatResponse(BaseChat):
    id: int
    name_chat: str
    type: ChatType = ChatType.PERSONAL
    creator_id: int