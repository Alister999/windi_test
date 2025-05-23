from typing import List
from src.models.user_association_group import user_group_association
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.general import Base
from src.models.user import User


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    name_group: Mapped[str] = mapped_column(unique=True, index=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    creator: Mapped["User"] = relationship()
    users: Mapped[List["User"]] = relationship(
        secondary=user_group_association,
        back_populates="groups",
        lazy="selectin"
    )