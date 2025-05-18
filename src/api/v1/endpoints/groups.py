import logging
from typing import List

from fastapi import APIRouter
from src.core.dependencies import SessionDep, AuthDep
from src.schemas.groups import GroupResponse, GroupCreate
from src.services.group_service import create_group_now, delete_group_now, change_group_now, get_groups_now, \
    get_group_now

router = APIRouter()
logger = logging.getLogger("ChatsEndpoint")


@router.post('/group', response_model=GroupResponse)
async def create_group(data: GroupCreate, db: SessionDep, current_user: AuthDep) -> GroupResponse:
    logger.info("Calling create group endpoint")
    result = await create_group_now(data, db)
    return result


@router.delete('/group/{group_id}')
async def delete_group(group_id: int, db: SessionDep, current_user: AuthDep) -> dict:
    logger.info("Calling delete group endpoint")
    result = await delete_group_now(group_id, db)
    return result



@router.put('/group/{group_id}', response_model=GroupResponse)
async def change_group(group_id: int, data: GroupCreate, db: SessionDep, current_user: AuthDep) -> GroupResponse:
    logger.info("Calling change group endpoint")
    result = await change_group_now(group_id, data, db)
    return result


@router.get('/group', response_model=List[GroupResponse])
async def get_groups(db: SessionDep, current_user: AuthDep) -> List[GroupResponse]:
    logger.info("Calling get groups endpoint")
    result = await get_groups_now(db)
    return result


@router.get('/group/{group_id}', response_model=GroupResponse)
async def get_group(group_id: int, db: SessionDep, current_user: AuthDep) -> GroupResponse:
    logger.info("Calling get group endpoint")
    result = await get_group_now(group_id, db)
    return result