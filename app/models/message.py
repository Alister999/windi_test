import enum
from datetime import datetime
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from app.models.chats import Chat
from app.models.general import Base
from app.models.user import User


class ReadType(enum.Enum):
    READED = 'readed'
    UNREADED = 'unreaded'


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    chat_id: Mapped["Chat"] = mapped_column(ForeignKey("chats.id"), nullable=False)
    sender_id: Mapped["User"] = mapped_column(ForeignKey("users.id"), nullable=False)
    text: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_read: Mapped[ReadType] = mapped_column(Enum(ReadType), default=ReadType.UNREADED, nullable=False)

