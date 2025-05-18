from pydantic import BaseModel, Field

from src.models.chats import ChatType


class BaseChat(BaseModel):
    class Config:
        from_attributes = True


class ChatCreate(BaseChat):
    name_chat: str = Field(max_length=50)
    type: ChatType = ChatType.PERSONAL
    creator_id: int


class ChatResponse(BaseChat):
    id: int
    name_chat: str
    type: ChatType = ChatType.PERSONAL
    creator_id: int