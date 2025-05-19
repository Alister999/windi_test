from typing import List
from src.models.user_association_group import user_group_association
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from src.models.general import Base
from src.models.user_assotiation_chat import user_chat_association


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    access_token: Mapped[str] = mapped_column(unique=True, nullable=True, default=None)
    refresh_token: Mapped[str] = mapped_column(unique=True, nullable=True, default=None, index=True)
    groups: Mapped[List["Group"]] = relationship(
        secondary=user_group_association,
        back_populates="users",
        lazy="selectin"
    )
    chats: Mapped[List["Chat"]] = relationship(
        secondary=user_chat_association,
        back_populates="users",
        lazy="selectin"
    )