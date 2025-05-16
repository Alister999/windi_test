from typing import List

from pydantic import BaseModel, Field

from app.schemas.users import UserResponse


class BaseGroup(BaseModel):
    class Config:
        from_attributes = True


class GroupCreate(BaseGroup):
    name_group: str = Field(max_length=50)
    creator_id: int
    user_ids: List[int]


class GroupResponse(BaseGroup):
    id: int
    name_group: str
    creator_id: int
    user_ids: List[UserResponse]