from typing import Annotated, Type

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.utils import get_current_user #, oauth2_scheme
from app.models.user import User

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#
# TokenDep = Annotated[str, Depends(oauth2_scheme)]
SessionDep = Annotated[AsyncSession, Depends(get_db)]

AuthDep = Annotated[User, Depends(get_current_user)]