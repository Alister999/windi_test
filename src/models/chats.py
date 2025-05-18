import enum
from typing import List

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.general import Base
from src.models.user_assotiation_chat import user_chat_association


class ChatType(enum.Enum):
    PERSONAL = "personal"
    GROUP = "group"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    name_chat: Mapped[str] = mapped_column(unique=True, index=True)
    type: Mapped[ChatType] = mapped_column(Enum(ChatType), default=ChatType.PERSONAL, nullable=False, index=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    users: Mapped[List["User"]] = relationship(
        secondary=user_chat_association,
        back_populates="chats",
        lazy="selectin"
    )