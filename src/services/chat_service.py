from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import ChatRepository, UserRepository
from src.models.chats import Chat
from src.models.user import User
from src.schemas.chats import ChatCreate, ChatResponse
from src.schemas.users import UserResponse


async def create_chat_now(data: ChatCreate, db: AsyncSession) -> ChatResponse:
    repo = ChatRepository(session=db)
    repo_users = UserRepository(session=db)
    check_chat = await repo.get_one_or_none(Chat.name_chat == data.name_chat)
    if check_chat:
        raise HTTPException(
            status_code=403,
            detail=f"Chat with name '{data.name_chat}' already exist"
        )
    check_user = await repo_users.get_one_or_none(User.id == data.creator_id)
    if not check_user:
        raise HTTPException(
            status_code=404,
            detail=f"User-creator with id '{data.creator_id}' not found"
        )

    users = []
    for user_id in data.user_ids:
        check_user = await repo_users.get_one_or_none(User.id == user_id)
        if not check_user:
            raise HTTPException(
                status_code=404,
                detail=f"User-participant with id '{user_id}' not found"
            )
        users.append(check_user)

    # updated_data = data.dict(exclude_unset=True)
    # new_chat = Chat()
    #
    # for key, value in updated_data.items():
    #     if key != "id":
    #         setattr(new_chat, key, value)

    new_chat = Chat(
        name_chat=data.name_chat,
        type=data.type,
        creator_id=data.creator_id,
        users=users
    )

    await repo.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)

    # re_formatted_chat = ChatResponse(
    #     id=new_chat.id,
    #     name_chat=new_chat.name_chat,
    #     creator_id=new_chat.creator_id,
    #     user_ids=[user.id for user in new_chat.users],
    # )

    re_formatted_chat = ChatResponse.model_validate(new_chat)

    return re_formatted_chat


async def delete_chat_now(chat_id: int, db: AsyncSession) -> dict:
    repo = ChatRepository(session=db)
    check_chat = await repo.get_one_or_none(Chat.id == chat_id)
    if not check_chat:
        raise HTTPException(
            status_code=404,
            detail=f"Chat with id '{chat_id}' is absent"
        )

    await repo.delete(chat_id)
    await db.commit()

    return {"message": f"Chat with id '{chat_id}' was deleted successful"}


async def change_chat_now(chat_id: int, data: ChatCreate, db: AsyncSession) -> ChatResponse:
    repo = ChatRepository(session=db)
    repo_users = UserRepository(session=db)
    check_chat = await repo.get_one_or_none(Chat.id == chat_id)
    if not check_chat:
        raise HTTPException(
            status_code=404,
            detail=f"Chat with id '{chat_id}' is absent"
        )
    check_chat_name = await repo.get_one_or_none(Chat.name_chat == data.name_chat)
    if check_chat_name:
        raise HTTPException(
            status_code=403,
            detail=f"Chat with name '{data.name_chat}' already exist"
        )
    check_user = await repo_users.get_one_or_none(User.id == data.creator_id)
    if not check_user:
        raise HTTPException(
            status_code=404,
            detail=f"User-creator with id '{data.creator_id}' not found"
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

    # re_formatted_chat = [ChatResponse(
    #     id=chat.id,
    #     name_chat=chat.name_chat,
    #     creator_id=chat.creator_id,
    #     user_ids=[user.id for user in chat.users],
    # ) for chat in get_chats]

    re_formatted_chat = [ChatResponse.model_validate(chat) for chat in get_chats]

    return re_formatted_chat


async def get_chat_now(chat_id: int, db: AsyncSession) -> ChatResponse:
    repo = ChatRepository(session=db)
    get_chat = await repo.get_one_or_none(Chat.id == chat_id)
    if not get_chat:
        raise HTTPException(
            status_code=404,
            detail=f"Chat with id '{chat_id}' not found"
        )

    re_formatted_chat = ChatResponse.model_validate(get_chat)
    #     = ChatResponse(
    #     id=get_chat.id,
    #     name_chat=get_chat.name_chat,
    #     creator_id=get_chat.creator_id,
    #     user_ids=[user.id for user in get_chat.users],
    # )

    return re_formatted_chat