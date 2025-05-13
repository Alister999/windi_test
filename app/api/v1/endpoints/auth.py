from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.users import UserResponse, UserCreate, UserLogin, RefreshToken
from app.services.auth_service import reg_user, login_user, refresh_my_token, get_users_all, get_current_user, \
    delete_current_user, change_current_user

router = APIRouter()

@router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    result = await reg_user(user, db)
    return result


@router.post('/login')
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)) -> dict:
    result = await login_user(user, db)
    return result


@router.post('/refresh')
async def refresh_token(data: RefreshToken, db: AsyncSession = Depends(get_db)) -> dict:
    result = await refresh_my_token(data, db)
    return result


@router.delete('/delete_user/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await delete_current_user(user_id, db)
    if result:
        return {"message": f"User with id {user_id} was deleted successful"}


@router.get('/user', response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)) -> List[UserResponse]:
    result = await get_users_all(db)
    return result


@router.get('/user/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    result = await get_current_user(user_id, db)
    return result


@router.put('/user/{user_id}', response_model=UserResponse)
async def change_user(data: UserCreate, user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    result = await change_current_user(data, user_id, db)
    return result