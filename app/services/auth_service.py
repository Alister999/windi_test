import os
from typing import List

from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db, UserRepository
from app.core.utils import verify_password, hash_password
from app.models.user import User
from app.schemas.users import UserResponse, UserCreate, UserLogin, RefreshToken
from app.services.auth_utils import create_access_token, create_refresh_token


async def reg_user(user: UserCreate, db: AsyncSession) -> UserResponse:
    repo = UserRepository(session=db)

    if await repo.get_one_or_none(User.name == user.name):
        raise HTTPException(
            status_code=403,
            detail=f"User with username '{user.name}' already exist"
        )

    if await repo.get_one_or_none(User.email == user.email):
        raise HTTPException(
            status_code=403,
            detail=f"User with email '{user.email}' already exist"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    await repo.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserResponse.model_validate(new_user)


async def login_user(user: UserLogin, db: AsyncSession) -> dict:
    repo = UserRepository(session=db)
    db_user = await repo.get_one_or_none(User.name == user.name)

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=403,
            detail='Invalid credentials'
        )

    access_token = create_access_token({"sub": db_user.name})
    refresh_token = create_refresh_token({"sub": db_user.name})

    db_user.access_token = access_token
    db_user.refresh_token = refresh_token

    await repo.update(db_user)
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_my_token(data: RefreshToken, db: AsyncSession) -> dict:
    repo = UserRepository(session=db)

    try:
        payload = jwt.decode(data.refresh_token, os.getenv("SECRET_KEY"), algorithms=[settings.ALGORITHM])
        name = payload.get("sub")
        if not name:
            raise HTTPException(
                status_code=403,
                detail='Invalid credentials'
            )
        new_access_token = create_access_token({"sub": name})

        db_user = await repo.get_one_or_none(User.refresh_token == data.refresh_token)
        if not db_user:
            raise HTTPException(
                status_code=404,
                detail='User not found'
            )

        db_user.access_token = new_access_token
        await repo.update(db_user)
        await db.commit()

        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail='Invalid refresh token'
        )


async def get_users_all(db: AsyncSession) -> List[UserResponse]:
    repo = UserRepository(session=db)
    db_users = await repo.list()
    re_formatted_users = [UserResponse.model_validate(db_user) for db_user in db_users]

    return re_formatted_users


async def get_current_user(user_id: int, db: AsyncSession) -> UserResponse:
    repo = UserRepository(session=db)
    getting_user = await repo.get_one_or_none(User.id == user_id)
    if not getting_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id '{user_id}' is absent"
        )

    re_formatted_user = UserResponse.model_validate(getting_user)

    return re_formatted_user


async def delete_current_user(user_id: int, db: AsyncSession) -> bool:
    repo = UserRepository(session=db)
    getting_user = await repo.get_one_or_none(User.id == user_id)
    if not getting_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id '{user_id}' is absent"
        )

    await repo.delete(user_id)
    await db.commit()

    return True


async def change_current_user(data: UserCreate, user_id: int, db: AsyncSession) -> UserResponse:
    repo = UserRepository(session=db)
    getting_user = await repo.get_one_or_none(User.id == user_id)
    if not getting_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id '{user_id}' is absent"
        )

    updated_data = data.dict(exclude_unset=True)
    if updated_data['name']:
        getting_name_user = await repo.get_one_or_none(User.name == updated_data['name'])
        if getting_name_user:
            raise HTTPException(
                status_code=400,
                detail=f"User with name '{updated_data['name']}' already exist"
            )
        else:
            getting_user.name = updated_data['name']
    if updated_data['email']:
        getting_name_email = await repo.get_one_or_none(User.email == updated_data['email'])
        if getting_name_email:
            raise HTTPException(
                status_code=400,
                detail=f"User with email '{updated_data['email']}' already exist"
            )
        else:
            getting_user.email = updated_data['email']
    if updated_data['password']:
        getting_user.password_hash = hash_password(updated_data['password'])

    await repo.update(getting_user)
    await db.commit()
    await db.refresh(getting_user)

    return UserResponse.model_validate(getting_user)