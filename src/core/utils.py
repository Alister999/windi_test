import logging
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.core.config import settings
from src.core.database import get_db, UserRepository
from src.models.user import User

load_dotenv()
logger = logging.getLogger("Utils")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    logger.info("Hashing password")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    logger.info("Check password")
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    logger.info("Try get current user")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[settings.ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            logger.error("Name is absent")
            raise credentials_exception
    except JWTError:
        logger.error("JWT error")
        raise credentials_exception

    repo = UserRepository(session=db)
    user = await repo.get_one_or_none(User.name == name)

    if user is None:
        logger.error("User is absent")
        raise credentials_exception
    return user


async def get_current_user_ws(token: str = Query(...), db: AsyncSession = Depends(get_db)) -> User:
    logger.info("Try get current user for WS")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_name: str = payload.get("sub")
        if user_name is None:
            logger.error("Username is absent")
            raise HTTPException(status_code=401, detail="Invalid token")
        user_repo = UserRepository(session=db)
        user = await user_repo.get_one_or_none(User.name == user_name)
        if user is None:
            logger.info("User is absent")
            raise HTTPException(status_code=401, detail="User not found")
        await db.refresh(user, attribute_names=["name", "id"])
        return user
    except ValueError as e:
        logger.error(f"Value error - {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        logger.error("JWT error")
        raise HTTPException(status_code=401, detail="Invalid token")