from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.groups import GroupResponse, GroupCreate
from app.services.group_service import create_group_now, delete_group_now, change_group_now, get_groups_now, \
    get_group_now

router = APIRouter()


@router.post('/group', response_model=GroupResponse)
async def create_group(data: GroupCreate, db: AsyncSession = Depends(get_db)) -> GroupResponse:
    result = await create_group_now(data, db)
    return result


@router.delete('/group/{group_id}')
async def delete_group(group_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await delete_group_now(group_id, db)
    return result



@router.put('/group/{group_id}', response_model=GroupResponse)
async def change_group(group_id: int, data: GroupCreate, db: AsyncSession = Depends(get_db)) -> GroupResponse:
    result = await change_group_now(group_id, data, db)
    return result


@router.get('/group', response_model=List[GroupResponse])
async def get_groups(db: AsyncSession = Depends(get_db)) -> List[GroupResponse]:
    result = await get_groups_now(db)
    return result


@router.get('/group/{group_id}', response_model=GroupResponse)
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)) -> GroupResponse:
    result = await get_group_now(group_id, db)
    return result