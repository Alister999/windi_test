from advanced_alchemy.config import SQLAlchemyAsyncConfig
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.chats import Chat
from src.models.general import Base
from src.models.group import Group
from src.models.message import Message
from src.models.user import User
from src.core.config import settings

load_dotenv()


database_url = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}'
sync_database_url = f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}'
if not database_url:
    raise ValueError("DATABASE_URL is not set in .env file")

db_config = SQLAlchemyAsyncConfig(connection_string=database_url)

async def get_db() -> AsyncSession:
    async with db_config.get_session() as session:
        yield session

async def init_db():
    async with db_config.get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User

class ChatRepository(SQLAlchemyAsyncRepository[Chat]):
    model_type = Chat

class GroupRepository(SQLAlchemyAsyncRepository[Group]):
    model_type = Group

class MessageRepository(SQLAlchemyAsyncRepository[Message]):
    model_type = Message