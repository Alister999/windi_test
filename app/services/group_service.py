from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import GroupRepository, UserRepository
from app.models.group import Group
from app.models.user import User
from app.schemas.groups import GroupCreate, GroupResponse
from app.schemas.users import UserResponse


async def create_group_now(data: GroupCreate, db: AsyncSession) -> GroupResponse:
    repo = GroupRepository(session=db)
    repo_users = UserRepository(session=db)
    check_group = await repo.get_one_or_none(Group.name_group == data.name_group)
    if check_group:
        raise HTTPException(
            status_code=403,
            detail=f"Group with name '{data.name_group}' already exist"
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
                detail=f"User-participant with id '{user_id}' not found"  # Исправлено: user_id вместо creator_id
            )
        users.append(check_user)

    new_group = Group(
        name_group=data.name_group,
        creator_id=data.creator_id,
        users=users
    )

    await repo.add(new_group)
    await db.commit()
    await db.refresh(new_group)

    re_formatted_group = GroupResponse(
        id=new_group.id,
        name_group=new_group.name_group,
        creator_id=new_group.creator_id,
        user_ids=[UserResponse.model_validate(user) for user in new_group.users]
    )

    return re_formatted_group


async def delete_group_now(group_id: int, db: AsyncSession) -> dict:
    repo = GroupRepository(session=db)
    check_group = await repo.get_one_or_none(Group.id == group_id)
    if not check_group:
        raise HTTPException(
            status_code=404,
            detail=f"Group with id '{group_id}' is absent"
        )

    await repo.delete(group_id)
    await db.commit()

    return {"message": f"Group with id '{group_id}' was deleted successful"}


async def change_group_now(group_id: int, data: GroupCreate, db: AsyncSession) -> GroupResponse:
    repo = GroupRepository(session=db)
    check_group = await repo.get_one_or_none(Group.id == group_id)
    if not check_group:
        raise HTTPException(
            status_code=404,
            detail=f"Group with id '{group_id}' is absent"
        )
    repo_users = UserRepository(session=db)
    check_user = await repo_users.get_one_or_none(User.id == data.creator_id)
    if not check_user:
        raise HTTPException(
            status_code=404,
            detail=f"User-creator with id '{data.creator_id}' not found"
        )
    check_group_name = await repo.get_one_or_none(Group.name_group == data.name_group)
    if check_group_name:
        raise HTTPException(
            status_code=403,
            detail=f"Group with name '{data.name_group}' already exist"
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

    check_group.name_group=data.name_group
    check_group.creator_id=data.creator_id
    check_group.users=users

    await repo.update(check_group)
    await db.commit()
    await db.refresh(check_group)

    re_formatted_group = GroupResponse(
        id=check_group.id,
        name_group=check_group.name_group,
        creator_id=check_group.creator_id,
        user_ids=[UserResponse.model_validate(user) for user in check_group.users]
    )

    return re_formatted_group


async def get_groups_now(db: AsyncSession) -> List[GroupResponse]:
    repo = GroupRepository(session=db)
    get_groups = await repo.list(load=(selectinload(Group.users),))

    re_formatted_groups = [
        GroupResponse(
            id=group.id,
            name_group=group.name_group,
            creator_id=group.creator_id,
            user_ids=[UserResponse.model_validate(user) for user in group.users]
        )
        for group in get_groups
    ]

    return re_formatted_groups


async def get_group_now(group_id: int, db: AsyncSession) -> GroupResponse:
    repo = GroupRepository(session=db)
    get_group = await repo.get_one_or_none(Group.id == group_id)
    if not get_group:
        raise HTTPException(
            status_code=404,
            detail=f"Group with id '{group_id}' not found"
        )

    re_formatted_group = GroupResponse(
        id=get_group.id,
        name_group=get_group.name_group,
        creator_id=get_group.creator_id,
        user_ids=[UserResponse.model_validate(user) for user in get_group.users]
    )


    return re_formatted_group