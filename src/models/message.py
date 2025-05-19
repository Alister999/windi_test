import enum
from datetime import datetime
from sqlalchemy import ForeignKey, Enum, String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from src.models.general import Base


class ReadType(enum.Enum):
    READ = 'read'
    UNREAD = 'unread'


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), nullable=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str]
    client_message_id: Mapped[str] = mapped_column(String(36), nullable=True, unique=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
    is_read: Mapped[ReadType] = mapped_column(Enum(ReadType), default=ReadType.UNREAD, nullable=False)

