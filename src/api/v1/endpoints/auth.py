import logging
from typing import List

from fastapi import APIRouter
from src.core.dependencies import SessionDep, AuthDep
from src.schemas.users import UserResponse, UserCreate, UserLogin, RefreshToken
from src.services.auth_service import reg_user, login_user, refresh_my_token, get_users_all , get_this_user, \
    delete_this_user, change_this_user

router = APIRouter()
logger = logging.getLogger("AuthEndpoint")

@router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate, db: SessionDep) -> UserResponse:
    logger.info("Calling register endpoint")
    result = await reg_user(user, db)
    return result


@router.post('/login')
async def login(user: UserLogin, db: SessionDep) -> dict:
    logger.info("Calling login endpoint")
    result = await login_user(user, db)
    return result


@router.post('/refresh')
async def refresh_token(data: RefreshToken, db: SessionDep) -> dict:
    logger.info("Calling refresh endpoint")
    result = await refresh_my_token(data, db)
    return result


@router.delete('/delete_user/{user_id}')
async def delete_user(user_id: int, db: SessionDep, current_user: AuthDep) -> dict[str, str] | None:
    logger.info("Calling delete user endpoint")
    result = await delete_this_user(user_id, db)
    if result:
        return {"message": f"User with id {user_id} was deleted successful"}


@router.get('/user', response_model=List[UserResponse])
async def get_users(db: SessionDep, current_user: AuthDep) -> List[UserResponse]: #, current_user: AuthDep
    logger.info("Calling get users endpoint")
    result = await get_users_all(db)
    return result


@router.get('/user/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, db: SessionDep, current_user: AuthDep) -> UserResponse:
    logger.info("Calling get user endpoint")
    result = await get_this_user(user_id, db)
    return result


@router.put('/user/{user_id}', response_model=UserResponse)
async def change_user(data: UserCreate, user_id: int, db: SessionDep, current_user: AuthDep) -> UserResponse:
    logger.info("Calling change user endpoint")
    result = await change_this_user(data, user_id, db)
    return result