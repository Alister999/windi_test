import logging
import os
from typing import List
from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.core.database import get_db, UserRepository
from src.core.utils import verify_password, hash_password
from src.models.user import User
from src.schemas.users import UserResponse, UserCreate, UserLogin, RefreshToken
from src.services.auth_utils import create_access_token, create_refresh_token


logger = logging.getLogger("AuthService")


async def reg_user(user: UserCreate, db: AsyncSession) -> UserResponse:
    repo = UserRepository(session=db)
    logger.info("Incoming to get user func")

    if await repo.get_one_or_none(User.name == user.name):
        logger.warning(f"User with username '{user.name}' already exist")
        raise HTTPException(
            status_code=403,
            detail=f"User with username '{user.name}' already exist"
        )

    if await repo.get_one_or_none(User.email == user.email):
        logger.warning(f"User with email '{user.email}' already exist")
        raise HTTPException(
            status_code=403,
            detail=f"User with email '{user.email}' already exist"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    logger.info("Add user to repo")
    await repo.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserResponse.model_validate(new_user)


async def login_user(user: UserLogin, db: AsyncSession) -> dict:
    logger.info("Incoming to login user func")
    repo = UserRepository(session=db)
    db_user = await repo.get_one_or_none(User.name == user.name)

    if not db_user or not verify_password(user.password, db_user.password_hash):
        logger.warning('Invalid credentials')
        raise HTTPException(
            status_code=403,
            detail='Invalid credentials'
        )

    access_token = create_access_token({"sub": db_user.name})
    refresh_token = create_refresh_token({"sub": db_user.name})

    db_user.access_token = access_token
    db_user.refresh_token = refresh_token

    logger.info("Update user to repo")
    await repo.update(db_user)
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_my_token(data: RefreshToken, db: AsyncSession) -> dict:
    logger.info("Incoming to refresh user token func")
    repo = UserRepository(session=db)

    try:
        payload = jwt.decode(data.refresh_token, os.getenv("SECRET_KEY"), algorithms=[settings.ALGORITHM])
        name = payload.get("sub")
        if not name:
            logger.warning('Invalid credentials')
            raise HTTPException(
                status_code=403,
                detail='Invalid credentials'
            )
        new_access_token = create_access_token({"sub": name})

        db_user = await repo.get_one_or_none(User.refresh_token == data.refresh_token)
        if not db_user:
            logger.warning('User not found')
            raise HTTPException(
                status_code=404,
                detail='User not found'
            )

        db_user.access_token = new_access_token

        logger.info("Update user to repo")
        await repo.update(db_user)
        await db.commit()

        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        logger.error('Invalid refresh token')
        raise HTTPException(
            status_code=403,
            detail='Invalid refresh token'
        )


async def get_users_all(db: AsyncSession) -> List[UserResponse]:
    logger.info("Incoming to get users func")
    repo = UserRepository(session=db)
    db_users = await repo.list()
    re_formatted_users = [UserResponse.model_validate(db_user) for db_user in db_users]

    return re_formatted_users


async def get_this_user(user_id: int, db: AsyncSession) -> UserResponse:
    logger.info("Incoming to get users func")
    repo = UserRepository(session=db)
    getting_user = await repo.get_one_or_none(User.id == user_id)
    if not getting_user:
        logger.warning(f"User with id '{user_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"User with id '{user_id}' is absent"
        )

    re_formatted_user = UserResponse.model_validate(getting_user)

    return re_formatted_user


async def delete_this_user(user_id: int, db: AsyncSession) -> bool:
    logger.info("Incoming to delete users func")
    repo = UserRepository(session=db)
    getting_user = await repo.get_one_or_none(User.id == user_id)
    if not getting_user:
        logger.warning(f"User with id '{user_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"User with id '{user_id}' is absent"
        )

    logger.info("Delete user from repo")
    await repo.delete(user_id)
    await db.commit()

    return True


async def change_this_user(data: UserCreate, user_id: int, db: AsyncSession) -> UserResponse:
    logger.info("Incoming to change users func")
    repo = UserRepository(session=db)
    getting_user = await repo.get_one_or_none(User.id == user_id)
    if not getting_user:
        logger.warning(f"User with id '{user_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"User with id '{user_id}' is absent"
        )

    updated_data = data.model_dump(exclude_unset=True)
    if updated_data['name']:
        getting_name_user = await repo.get_one_or_none(User.name == updated_data['name'])
        if getting_name_user:
            logger.warning(f"User with name '{updated_data['name']}' already exist")
            raise HTTPException(
                status_code=400,
                detail=f"User with name '{updated_data['name']}' already exist"
            )
        else:
            getting_user.name = updated_data['name']
    if updated_data['email']:
        getting_name_email = await repo.get_one_or_none(User.email == updated_data['email'])
        if getting_name_email:
            logger.warning(f"User with email '{updated_data['email']}' already exist")
            raise HTTPException(
                status_code=400,
                detail=f"User with email '{updated_data['email']}' already exist"
            )
        else:
            getting_user.email = updated_data['email']
    if updated_data['password']:
        getting_user.password_hash = hash_password(updated_data['password'])

    logger.info("Update user to repo")
    await repo.update(getting_user)
    await db.commit()
    await db.refresh(getting_user)

    return UserResponse.model_validate(getting_user)