from fastapi import APIRouter

from .endpoints import auth, chats, groups, messages, socket

router = APIRouter(prefix="/v1")

router.include_router(auth.router, tags=["Auth"])
router.include_router(chats.router, tags=["Chats"])
router.include_router(groups.router, tags=["Groups"])
router.include_router(messages.router, tags=["Messages"])
router.include_router(socket.router, tags=["WebSoket"])