import enum
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.models.general import Base


class ChatType(enum.Enum):
    PERSONAL = "personal"
    GROUP = "group"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    name_chat: Mapped[str] = mapped_column(unique=True, index=True)
    type: Mapped[ChatType] = mapped_column(Enum(ChatType), default=ChatType.PERSONAL, nullable=False, index=True)