from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.database import get_db
# from app.schemas.user import UserResponse, UserCreate, UserLogin, RefreshToken
# from app.services.auth_service import reg_user, login_user, refresh_my_token

router = APIRouter()


@router.post('/message')#, response_model=UserResponse)
async def create_message(): #user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    # result = await reg_user(user, db)
    # return result
    pass


@router.delete('/message/{int: id}')
async def delete_message(id: int):
    pass


@router.put('/message/{int: id}')
async def change_message(id: int):
    pass


@router.get('/message')
async def get_messages():
    pass


@router.get('/message/{int: id}')
async def get_message(id: int):
    pass