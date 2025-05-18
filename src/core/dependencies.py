from typing import Annotated, Type

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.utils import get_current_user #, oauth2_scheme
from src.models.user import User

SessionDep = Annotated[AsyncSession, Depends(get_db)]

AuthDep = Annotated[User, Depends(get_current_user)]