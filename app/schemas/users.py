from pydantic import BaseModel

class BaseUser(BaseModel):
    class Config:
        from_attributes = True


class UserCreate(BaseUser):
    name: str
    email: str
    password: str


class UserLogin(BaseUser):
    name: str
    password: str

class UserResponse(BaseUser):
    id: int
    name: str
    email: str
    password_hash: str


class RefreshToken(BaseUser):
    refresh_token: str