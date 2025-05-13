from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.general import Base
from app.models.user import User


# chat_user_association = Table(
#     "chat_user_association",
#     Base.metadata,
#     Column("chat_id", ForeignKey("chats.id"), primary_key=True),
#     Column("user_id", ForeignKey("users.id"), primary_key=True),
# )


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    name_group: Mapped[str] = mapped_column(unique=True, index=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # creator: Mapped["User"] = relationship(back_populates='groups')
    # participants: Mapped[list["User"]] = relationship(
    #     secondary="user_association_group",
    #     back_populates="chats",
    #     viewonly=True
    # )





