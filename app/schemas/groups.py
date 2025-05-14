from pydantic import BaseModel


class BaseGroup(BaseModel):
    class Config:
        from_attributes = True


class GroupCreate(BaseGroup):
    name_group: str
    creator_id: int


class GroupResponse(BaseGroup):
    id: int
    name_group: str
    creator_id: int