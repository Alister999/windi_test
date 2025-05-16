from typing import List

from fastapi import APIRouter

from app.core.dependencies import SessionDep, AuthDep
from app.schemas.messages import MessageResponse, MessageCreate
from app.services.message_service import create_message_now, delete_message_now, change_message_now, get_messages_now, \
    get_message_now

router = APIRouter()


@router.post('/message', response_model=MessageResponse)
async def create_message(data: MessageCreate, db: SessionDep, current_user: AuthDep) -> MessageResponse:
    result = await create_message_now(data, db)
    return result


@router.delete('/message/{message_id}')
async def delete_message(message_id: int, db: SessionDep, current_user: AuthDep) -> dict:
    result = await delete_message_now(message_id, db)
    return result


@router.put('/message/{message_id}', response_model=MessageResponse)
async def change_message(message_id: int, data: MessageCreate, db: SessionDep, current_user: AuthDep) -> MessageResponse:
    result = await change_message_now(message_id, data, db)
    return result


@router.get('/message', response_model=List[MessageResponse])
async def get_messages(db: SessionDep, current_user: AuthDep) -> List[MessageResponse]:
    result = await get_messages_now(db)
    return result


@router.get('/message/{message_id}', response_model=MessageResponse)
async def get_message(message_id: int, db: SessionDep, current_user: AuthDep) -> MessageResponse:
    result = await get_message_now(message_id, db)
    return result