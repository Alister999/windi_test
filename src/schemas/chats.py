from typing import List
from pydantic import BaseModel, Field
from src.models.chats import ChatType
from src.schemas.users import UserResponse


class BaseChat(BaseModel):
    class Config:
        from_attributes = True


class ChatCreate(BaseChat):
    name_chat: str = Field(max_length=50)
    type: ChatType = ChatType.PERSONAL
    creator_id: int
    user_ids: List[int]


class ChatResponse(BaseChat):
    id: int
    name_chat: str
    type: ChatType = ChatType.PERSONAL
    creator_id: int
    users: List[UserResponse]