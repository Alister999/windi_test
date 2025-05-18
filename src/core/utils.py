import os

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, FastAPI, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.config import settings
from src.core.database import init_db, get_db, UserRepository  # , UserRepository
# from src.core.dependencies import SessionDep
from src.models.user import User

load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[settings.ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    repo = UserRepository(session=db)
    user = await repo.get_one_or_none(User.name == name)

    if user is None:
        raise credentials_exception
    return user

async def get_current_user_ws(token: str = Query(...), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_name: str = payload.get("sub")
        if user_name is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_repo = UserRepository(session=db) #SQLAlchemyAsyncRepository[User](session=db, model_type=User)
        user = await user_repo.get_one_or_none(User.name == user_name)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        await db.refresh(user, attribute_names=["name", "id"])
        return user
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")