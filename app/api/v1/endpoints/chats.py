from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.chats import ChatResponse, ChatCreate
from app.services.chat_service import create_chat_now, delete_chat_now, change_chat_now, get_chats_now, get_chat_now

router = APIRouter()


@router.post('/chat', response_model=ChatResponse)
async def create_chat(data: ChatCreate, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    result = await create_chat_now(data, db)
    return result


@router.delete('/chat/{chat_id}')
async def delete_chat(chat_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await delete_chat_now(chat_id, db)
    return result


@router.put('/chat/{chat_id}', response_model=ChatResponse)
async def change_chat(chat_id: int, data: ChatCreate, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    result = await change_chat_now(chat_id, data, db)
    return result


@router.get('/chat', response_model=List[ChatResponse])
async def get_chats(db: AsyncSession = Depends(get_db)) -> List[ChatResponse]:
    result = await get_chats_now(db)
    return result


@router.get('/chat/{chat_id}', response_model=ChatResponse)
async def get_chat(chat_id: int, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    result = await get_chat_now(chat_id, db)
    return result