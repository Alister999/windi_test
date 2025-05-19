from pydantic import BaseModel, Field, EmailStr


class BaseUser(BaseModel):
    class Config:
        from_attributes = True


class UserCreate(BaseUser):
    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    password: str = Field(max_length=50)


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