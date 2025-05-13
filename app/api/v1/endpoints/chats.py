from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.database import get_db
# from app.schemas.user import UserResponse, UserCreate, UserLogin, RefreshToken
# from app.services.auth_service import reg_user, login_user, refresh_my_token

router = APIRouter()


@router.post('/chat')#, response_model=UserResponse)
async def create_chat(): #user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    # result = await reg_user(user, db)
    # return result
    pass


@router.delete('/chat/{int: id}')
async def delete_chat(id: int):
    pass


@router.put('/chat/{int: id}')
async def change_chat(id: int):
    pass


@router.get('/chat')
async def get_chats():
    pass


@router.get('/chat/{int: id}')
async def get_chat(id: int):
    pass