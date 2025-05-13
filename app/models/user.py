from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.models.general import Base
# from app.models.group import Group


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    access_token: Mapped[str] = mapped_column(unique=True, nullable=True, default=None)
    refresh_token: Mapped[str] = mapped_column(unique=True, nullable=True, default=None, index=True)
    # chats: Mapped[list["Group"]] = relationship(
    #     secondary="user_association_group",
    #     back_populates="participants",
    #     viewonly=True
    # )