from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import ChatRepository
from app.models.chats import Chat
from app.schemas.chats import ChatCreate, ChatResponse


async def create_chat_now(data: ChatCreate, db: AsyncSession) -> ChatResponse:
    repo = ChatRepository(session=db)
    check_chat = await repo.get_one_or_none(Chat.name_chat == data.name_chat)
    if check_chat:
        raise HTTPException(
            status_code=403,
            detail=f'Chat with name {data.name_chat} already exist'
        )

    updated_data = data.dict(exclude_unset=True)
    new_chat = Chat()

    for key, value in updated_data.items():
        if key != "id":
            setattr(new_chat, key, value)

    await repo.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)

    re_formatted_chat = ChatResponse.model_validate(new_chat)

    return re_formatted_chat


async def delete_chat_now(chat_id: int, db: AsyncSession) -> dict:
    repo = ChatRepository(session=db)
    check_chat = await repo.get_one_or_none(Chat.id == chat_id)
    if not check_chat:
        raise HTTPException(
            status_code=404,
            detail=f'Chat with id {chat_id} is absent'
        )

    await repo.delete(chat_id)
    await db.commit()

    return {"message": f"Chat with id {chat_id} was deleted successful"}


async def change_chat_now(chat_id: int, data: ChatCreate, db: AsyncSession) -> ChatResponse:
    repo = ChatRepository(session=db)
    check_chat = await repo.get_one_or_none(Chat.id == chat_id)
    if not check_chat:
        raise HTTPException(
            status_code=404,
            detail=f'Chat with id {chat_id} is absent'
        )
    check_chat_name = await repo.get_one_or_none(Chat.name_chat == data.name_chat)
    if check_chat_name:
        raise HTTPException(
            status_code=403,
            detail=f'Chat with name {data.name_chat} already exist'
        )

    updated_data = data.dict(exclude_unset=True)

    for key, value in updated_data.items():
        if key != "id":
            setattr(check_chat, key, value)

    await repo.update(check_chat)
    await db.commit()
    await db.refresh(check_chat)

    re_formatted_chat = ChatResponse.model_validate(check_chat)

    return re_formatted_chat


async def get_chats_now(db: AsyncSession) -> List[ChatResponse]:
    repo = ChatRepository(session=db)
    get_chats = await repo.list()

    re_formatted_chats = [ChatResponse.model_validate(chat) for chat in get_chats]

    return re_formatted_chats


async def get_chat_now(chat_id: int, db: AsyncSession) -> ChatResponse:
    repo = ChatRepository(session=db)
    get_chat = await repo.get_one_or_none(Chat.id == chat_id)
    if not get_chat:
        raise HTTPException(
            status_code=404,
            detail=f'Chat with id {chat_id} not found'
        )

    re_formatted_chat = ChatResponse.model_validate(get_chat)

    return re_formatted_chat