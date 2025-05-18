from fastapi import APIRouter, WebSocket, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.ConnectionManager import ConnectionManager
from src.core.database import get_db, GroupRepository, ChatRepository
from src.core.utils import get_current_user_ws
from src.models.chats import Chat
from src.models.group import Group
from src.models.user import User
import logging

from src.services.web_socket_service import get_group_user_ids, get_direct_chat_user_ids, group_connection, \
    chat_connection

logger = logging.Logger(__name__)

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/group/{group_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        group_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_ws)
):

    logger.info(f"Connecting user (name: {current_user.name}, id: {current_user.id})")
    try:
        repo_group = GroupRepository(session=db)
        check_group = await repo_group.get_one_or_none(Group.id == group_id)
        if not check_group:
            logger.error(f"Group is absent: id={group_id}")
            await websocket.accept()
            raise HTTPException(
                status_code=404,
                detail=f"Group with id '{group_id}' not found"
            )

        user_ids = await get_group_user_ids(db, group_id)
        if current_user.id not in user_ids:
            logger.error(f"User {current_user.name} (id: {current_user.id}) not in group {group_id}")
            await websocket.accept()
            raise HTTPException(
                status_code=401,
                detail=f"User {current_user.name} (id: {current_user.id}) not in group {group_id}"
            )

        await manager.connect(websocket, group_id, current_user.id)
        logger.info(f"Group id - {group_id}, username - {current_user.name}")

        await group_connection(websocket, group_id, current_user, db, user_ids, manager)

    except HTTPException as e:
        logger.error(f"HTTP error: {e.status_code} - {e.detail}")
        websocket_close_code = (
            1003 if e.status_code == 404 else
            1008 if e.status_code == 401 else
            1007 if e.status_code == 400 else
            1000
        )
        await websocket.accept()
        await websocket.send_json({"error": e.detail})
        await websocket.close(code=websocket_close_code)
        return
    except Exception as e:
        logger.error(f"Unexpected error for user {current_user.name} in direct group : {str(e)}") #{chat_id}
        await websocket.accept()
        await websocket.send_json({"error": "Internal server error"})
        await websocket.close(code=1000)
        return


@router.websocket("/ws/chat/{chat_id}")
async def websocket_direct_endpoint(
        websocket: WebSocket,
        chat_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_ws)
):
    logger.info(f"Connecting user (name: {current_user.name}, id: {current_user.id})")

    repo_chat = ChatRepository(session=db)
    check_chat = await repo_chat.get_one_or_none(Chat.id == chat_id)
    if not check_chat:
        logger.error(f"Direct chat is absent: id={chat_id}")
        await websocket.accept()
        raise HTTPException(
            status_code=404,
            detail=f"Direct chat with id '{chat_id}' not found"
        )

    user_ids = await get_direct_chat_user_ids(db, chat_id)
    if current_user.id not in user_ids:
        logger.error(f"User {current_user.name} (id: {current_user.id}) not in direct chat {chat_id}")
        await websocket.accept()
        raise HTTPException(
            status_code=401,
            detail=f"User {current_user.name} (id: {current_user.id}) not in direct chat {chat_id}"
        )

    if len(user_ids) != 2:
        logger.error(f"Direct chat {chat_id} has invalid number of users: {len(user_ids)}")
        await websocket.accept()
        raise HTTPException(
            status_code=403,
            detail=f"Direct chat {chat_id} has invalid number of users: {len(user_ids)}"
        )

    await manager.connect(websocket, chat_id, current_user.id)
    logger.info(f"Direct chat id - {chat_id}, username - {current_user.name}")

    await chat_connection(websocket, chat_id, current_user, db, user_ids, manager)