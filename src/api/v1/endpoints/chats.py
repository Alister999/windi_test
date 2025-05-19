import logging
from typing import List

from fastapi import APIRouter
from src.core.dependencies import SessionDep, AuthDep
from src.schemas.chats import ChatResponse, ChatCreate
from src.services.chat_service import create_chat_now, delete_chat_now, change_chat_now, get_chats_now, get_chat_now

router = APIRouter()
logger = logging.getLogger("ChatsEndpoint")


@router.post('/chat', response_model=ChatResponse)
async def create_chat(data: ChatCreate, db: SessionDep, current_user: AuthDep) -> ChatResponse:
    logger.info("Calling add chat endpoint")
    result = await create_chat_now(data, db)
    return result


@router.delete('/chat/{chat_id}')
async def delete_chat(chat_id: int, db: SessionDep, current_user: AuthDep) -> dict:
    logger.info("Calling delete chat endpoint")
    result = await delete_chat_now(chat_id, db)
    return result


@router.put('/chat/{chat_id}', response_model=ChatResponse)
async def change_chat(chat_id: int, data: ChatCreate, db: SessionDep, current_user: AuthDep) -> ChatResponse:
    logger.info("Calling change chat endpoint")
    result = await change_chat_now(chat_id, data, db)
    return result


@router.get('/chat', response_model=List[ChatResponse])
async def get_chats(db: SessionDep, current_user: AuthDep) -> List[ChatResponse]:
    logger.info("Calling get chats endpoint")
    result = await get_chats_now(db)
    return result


@router.get('/chat/{chat_id}', response_model=ChatResponse)
async def get_chat(chat_id: int, db: SessionDep, current_user: AuthDep) -> ChatResponse:
    logger.info("Calling get chat endpoint")
    result = await get_chat_now(chat_id, db)
    return result