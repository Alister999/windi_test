import logging
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
from jose import jwt
from src.core.config import settings


load_dotenv()
logger = logging.getLogger("AuthUtils")


def create_access_token(data: dict):
    logger.info("Incoming to create access token func")
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict):
    logger.info("Incoming to refresh access token func")
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)