import enum
from datetime import datetime
from sqlalchemy import ForeignKey, Enum, String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from src.models.chats import Chat
from src.models.general import Base
from src.models.user import User


class ReadType(enum.Enum):
    READ = 'read'
    UNREAD = 'unread'


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    text: Mapped[str]
    client_message_id: Mapped[str] = mapped_column(String(36), nullable=True, unique=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_read: Mapped[ReadType] = mapped_column(Enum(ReadType), default=ReadType.UNREAD, nullable=False)

