from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.models.general import Base


class UserAssociationGroup(Base):
    __tablename__ = "user_association_group"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
