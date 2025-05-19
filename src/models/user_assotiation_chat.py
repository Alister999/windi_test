from sqlalchemy import Column, Table, Integer, ForeignKey


from src.models.general import Base
user_chat_association = Table(
    "user_chat_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("chat_id", Integer, ForeignKey("chats.id"), primary_key=True),
)