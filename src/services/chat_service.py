import logging
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import ChatRepository, UserRepository
from src.models.chats import Chat
from src.models.user import User
from src.schemas.chats import ChatCreate, ChatResponse


logger = logging.getLogger("ChatService")


async def create_chat_now(data: ChatCreate, db: AsyncSession) -> ChatResponse:
    logger.info("Incoming to create chat func")
    repo = ChatRepository(session=db)
    repo_users = UserRepository(session=db)
    check_chat = await repo.get_one_or_none(Chat.name_chat == data.name_chat)
    if check_chat:
        logger.warning(f"Chat with name '{data.name_chat}' already exist")
        raise HTTPException(
            status_code=403,
            detail=f"Chat with name '{data.name_chat}' already exist"
        )
    check_user = await repo_users.get_one_or_none(User.id == data.creator_id)
    if not check_user:
        logger.warning(f"User-creator with id '{data.creator_id}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"User-creator with id '{data.creator_id}' not found"
        )

    users = []
    for user_id in data.user_ids:
        check_user = await repo_users.get_one_or_none(User.id == user_id)
        if not check_user:
            logger.warning(f"User-participant with id '{user_id}' not found")
            raise HTTPException(
                status_code=404,
                detail=f"User-participant with id '{user_id}' not found"
            )
        users.append(check_user)

    new_chat = Chat(
        name_chat=data.name_chat,
        type=data.type,
        creator_id=data.creator_id,
        users=users
    )

    logger.info("Add chat to repo")
    await repo.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)

    re_formatted_chat = ChatResponse.model_validate(new_chat)

    return re_formatted_chat


async def delete_chat_now(chat_id: int, db: AsyncSession) -> dict:
    logger.info("Incoming to delete chat func")
    repo = ChatRepository(session=db)
    check_chat = await repo.get_one_or_none(Chat.id == chat_id)
    if not check_chat:
        logger.warning(f"Chat with id '{chat_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Chat with id '{chat_id}' is absent"
        )

    logger.info("Delete chat from repo")
    await repo.delete(chat_id)
    await db.commit()

    return {"message": f"Chat with id '{chat_id}' was deleted successful"}


async def change_chat_now(chat_id: int, data: ChatCreate, db: AsyncSession) -> ChatResponse:
    logger.info("Incoming to change chat func")
    repo = ChatRepository(session=db)
    repo_users = UserRepository(session=db)
    check_chat = await repo.get_one_or_none(Chat.id == chat_id)
    if not check_chat:
        logger.warning(f"Chat with id '{chat_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Chat with id '{chat_id}' is absent"
        )
    check_chat_name = await repo.get_one_or_none(Chat.name_chat == data.name_chat)
    if check_chat_name:
        logger.warning(f"Chat with name '{data.name_chat}' already exist")
        raise HTTPException(
            status_code=403,
            detail=f"Chat with name '{data.name_chat}' already exist"
        )
    check_user = await repo_users.get_one_or_none(User.id == data.creator_id)
    if not check_user:
        logger.warning(f"User-creator with id '{data.creator_id}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"User-creator with id '{data.creator_id}' not found"
        )

    updated_data = data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        if key != "id":
            setattr(check_chat, key, value)

    logger.info("Update chat in repo")
    await repo.update(check_chat)
    await db.commit()
    await db.refresh(check_chat)

    re_formatted_chat = ChatResponse.model_validate(check_chat)

    return re_formatted_chat


async def get_chats_now(db: AsyncSession) -> List[ChatResponse]:
    logger.info("Incoming to get chats func")
    repo = ChatRepository(session=db)
    get_chats = await repo.list()

    re_formatted_chat = [ChatResponse.model_validate(chat) for chat in get_chats]

    return re_formatted_chat


async def get_chat_now(chat_id: int, db: AsyncSession) -> ChatResponse:
    logger.info("Incoming to get chat func")
    repo = ChatRepository(session=db)
    get_chat = await repo.get_one_or_none(Chat.id == chat_id)
    if not get_chat:
        logger.warning(f"Chat with id '{chat_id}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"Chat with id '{chat_id}' not found"
        )

    re_formatted_chat = ChatResponse.model_validate(get_chat)

    return re_formatted_chat