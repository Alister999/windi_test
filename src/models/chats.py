import enum
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.models.general import Base


class ChatType(enum.Enum):
    PERSONAL = "personal"
    GROUP = "group"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    name_chat: Mapped[str] = mapped_column(unique=True, index=True)
    type: Mapped[ChatType] = mapped_column(Enum(ChatType), default=ChatType.PERSONAL, nullable=False, index=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)