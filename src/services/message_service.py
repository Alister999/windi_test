import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import MessageRepository, UserRepository, ChatRepository, GroupRepository
from src.models.chats import Chat
from src.models.group import Group
from src.models.message import Message
from src.models.user import User
from src.schemas.messages import MessageCreate, MessageResponse, MessageHistory, MessageCreateGroup

logger = logging.getLogger("MessageService")


async def create_message_now(data: MessageCreate | MessageCreateGroup, db: AsyncSession) -> MessageResponse:
    logger.info("Incoming to create message func")
    repo = MessageRepository(session=db)
    repo_users = UserRepository(session=db)
    repo_chat = ChatRepository(session=db)
    repo_group = GroupRepository(session=db)
    check_user = await repo_users.get_one_or_none(User.id == data.sender_id)
    if not check_user:
        logger.warning(f"User-sender with id '{data.sender_id}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"User-sender with id '{data.sender_id}' not found"
        )

    if isinstance(data, MessageCreate):
        logger.info("Creating message for chat")
        check_chat = await repo_chat.get_one_or_none(Chat.id == data.chat_id)
        if not check_chat:
            logger.warning(f"Chat with id '{data.chat_id}' not found")
            raise HTTPException(
                status_code=404,
                detail=f"Chat with id '{data.chat_id}' not found"
            )
    else:
        logger.info("Creating message for group")
        check_group = await repo_group.get_one_or_none(Group.id == data.group_id)
        if not check_group:
            logger.warning(f"Group with id '{data.group_id}' not found")
            raise HTTPException(
                status_code=404,
                detail=f"Group with id '{data.group_id}' not found"
            )

    updated_data = data.dict(exclude_unset=True)
    new_message = Message()

    for key, value in updated_data.items():
        if key != "id":
            setattr(new_message, key, value)

    logger.info("Add message to repo")
    await repo.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    re_formatted_message = MessageResponse.model_validate(new_message)

    return re_formatted_message


async def delete_message_now(message_id: int, db: AsyncSession) -> dict:
    logger.info("Incoming to delete message func")
    repo = MessageRepository(session=db)
    check_message = await repo.get_one_or_none(Message.id == message_id)
    if not check_message:
        logger.warning(f"Message with id '{message_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Message with id '{message_id}' is absent"
        )

    logger.info("Delete message from repo")
    await repo.delete(message_id)
    await db.commit()

    return {"message": f"Message with id '{message_id}' was deleted successful"}


async def change_message_now(message_id: int, data: MessageCreate, db: AsyncSession) -> MessageResponse:
    logger.info("Incoming to change message func")
    repo = MessageRepository(session=db)
    repo_users = UserRepository(session=db)
    repo_chat = ChatRepository(session=db)
    check_user = await repo_users.get_one_or_none(User.id == data.sender_id)
    if not check_user:
        logger.warning(f"User-sender with id '{data.sender_id}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"User-sender with id '{data.sender_id}' not found"
        )
    check_chat = await repo_chat.get_one_or_none(Chat.id == data.chat_id)
    if not check_chat:
        logger.warning(f"Chat with id '{data.chat_id}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"Chat with id '{data.chat_id}' not found"
        )
    check_message = await repo.get_one_or_none(Message.id == message_id)
    if not check_message:
        logger.warning(f"Message with id '{message_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Message with id '{message_id}' is absent"
        )

    updated_data = data.dict(exclude_unset=True)

    for key, value in updated_data.items():
        if key != "id":
            setattr(check_message, key, value)

    logger.info("Update message to repo")
    await repo.update(check_message)
    await db.commit()
    await db.refresh(check_message)

    re_formatted_message = MessageResponse.model_validate(check_message)

    return re_formatted_message


async def get_messages_now(db: AsyncSession) -> List[MessageResponse]:
    logger.info("Incoming to get messages func")
    repo = MessageRepository(session=db)
    get_messages = await repo.list()

    re_formatted_messages = [MessageResponse.model_validate(message) for message in get_messages]

    return re_formatted_messages


async def get_message_now(message_id: int, db: AsyncSession) -> MessageResponse:
    logger.info("Incoming to get message func")
    repo = MessageRepository(session=db)
    get_message = await repo.get_one_or_none(Message.id == message_id)
    if not get_message:
        logger.warning(f"Message with id '{message_id}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"Message with id '{message_id}' not found"
        )

    re_formatted_message = MessageResponse.model_validate(get_message)

    return re_formatted_message


async def get_messages_history(
        db: AsyncSession,
        chat_id: int,
        limit: int = 50,
        offset: int = 0,
) -> List[MessageHistory]:
    logger.info("Incoming to get messages history func")

    query = select(Message).where(Message.chat_id == chat_id).order_by(Message.timestamp.asc()).limit(limit).offset(
        offset)
    result = await db.execute(query)
    messages = result.scalars().all()
    if not messages:
        logger.warning("No messages found")
        raise HTTPException(
            status_code=404,
            detail="No messages found"
        )

    formatted_messages = [MessageHistory.model_validate(message) for message in messages]

    return formatted_messages