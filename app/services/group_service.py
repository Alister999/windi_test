from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import GroupRepository, UserRepository
from app.models.group import Group
from app.models.user import User
from app.schemas.groups import GroupCreate, GroupResponse


async def create_group_now(data: GroupCreate, db: AsyncSession) -> GroupResponse:
    repo = GroupRepository(session=db)
    repo_users = UserRepository(session=db)
    check_group = await repo.get_one_or_none(Group.name_group == data.name_group)
    if check_group:
        raise HTTPException(
            status_code=403,
            detail=f'Group with name {data.name_group} already exist'
        )
    check_user = await repo_users.get_one_or_none(User.id == data.creator_id)
    if not check_user:
        raise HTTPException(
            status_code=404,
            detail=f'User-creator with id {data.creator_id} not found'
        )

    updated_data = data.dict(exclude_unset=True)
    new_group = Group()

    for key, value in updated_data.items():
        if key != "id":
            setattr(new_group, key, value)

    await repo.add(new_group)
    await db.commit()
    await db.refresh(new_group)

    re_formatted_group = GroupResponse.model_validate(new_group)

    return re_formatted_group


async def delete_group_now(group_id: int, db: AsyncSession) -> dict:
    repo = GroupRepository(session=db)
    check_group = await repo.get_one_or_none(Group.id == group_id)
    if not check_group:
        raise HTTPException(
            status_code=404,
            detail=f'Group with id {group_id} is absent'
        )

    await repo.delete(group_id)
    await db.commit()

    return {"message": f"Group with id {group_id} was deleted successful"}


async def change_group_now(group_id: int, data: GroupCreate, db: AsyncSession) -> GroupResponse:
    repo = GroupRepository(session=db)
    check_group = await repo.get_one_or_none(Group.id == group_id)
    if not check_group:
        raise HTTPException(
            status_code=404,
            detail=f'Group with id {group_id} is absent'
        )
    repo_users = UserRepository(session=db)
    check_user = await repo_users.get_one_or_none(User.id == data.creator_id)
    if not check_user:
        raise HTTPException(
            status_code=404,
            detail=f'User-creator with id {data.creator_id} not found'
        )
    check_group_name = await repo.get_one_or_none(Group.name_group == data.name_group)
    if check_group_name:
        raise HTTPException(
            status_code=403,
            detail=f'Group with name {data.name_group} already exist'
        )

    updated_data = data.dict(exclude_unset=True)

    for key, value in updated_data.items():
        if key != "id":
            setattr(check_group, key, value)

    await repo.update(check_group)
    await db.commit()
    await db.refresh(check_group)

    re_formatted_group = GroupResponse.model_validate(check_group)

    return re_formatted_group


async def get_groups_now(db: AsyncSession) -> List[GroupResponse]:
    repo = GroupRepository(session=db)
    get_groups = await repo.list()

    re_formatted_groups = [GroupResponse.model_validate(group) for group in get_groups]

    return re_formatted_groups


async def get_group_now(group_id: int, db: AsyncSession) -> GroupResponse:
    repo = GroupRepository(session=db)
    get_group = await repo.get_one_or_none(Group.id == group_id)
    if not get_group:
        raise HTTPException(
            status_code=404,
            detail=f'Group with id {group_id} not found'
        )

    re_formatted_group = GroupResponse.model_validate(get_group)

    return re_formatted_group