import logging
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.core.database import GroupRepository, UserRepository
from src.models.group import Group
from src.models.user import User
from src.schemas.groups import GroupCreate, GroupResponse
from src.schemas.users import UserResponse


logger = logging.getLogger("GroupService")


async def create_group_now(data: GroupCreate, db: AsyncSession) -> GroupResponse:
    logger.info("Incoming to create group func")
    repo = GroupRepository(session=db)
    repo_users = UserRepository(session=db)
    check_group = await repo.get_one_or_none(Group.name_group == data.name_group)
    if check_group:
        logger.warning(f"Group with name '{data.name_group}' already exist")
        raise HTTPException(
            status_code=403,
            detail=f"Group with name '{data.name_group}' already exist"
        )
    check_user = await repo_users.get_one_or_none(User.id == data.creator_id)
    if not check_user:
        logger.warning(f"User-creator with id '{data.creator_id}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"User-creator with id '{data.creator_id}' not found"
        )

    users = []
    for user_id in data.user_ids:
        check_user = await repo_users.get_one_or_none(User.id == user_id)
        if not check_user:
            logger.warning(f"User-participant with id '{user_id}' not found")
            raise HTTPException(
                status_code=404,
                detail=f"User-participant with id '{user_id}' not found"
            )
        users.append(check_user)

    new_group = Group(
        name_group=data.name_group,
        creator_id=data.creator_id,
        users=users
    )

    logger.info("Add group to repo")
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
    logger.info("Incoming to delete group func")
    repo = GroupRepository(session=db)
    check_group = await repo.get_one_or_none(Group.id == group_id)
    if not check_group:
        logger.warning(f"Group with id '{group_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Group with id '{group_id}' is absent"
        )

    await repo.delete(group_id)
    await db.commit()

    return {"message": f"Group with id '{group_id}' was deleted successful"}


async def change_group_now(group_id: int, data: GroupCreate, db: AsyncSession) -> GroupResponse:
    logger.info("Incoming to change group func")
    repo = GroupRepository(session=db)
    check_group = await repo.get_one_or_none(Group.id == group_id)
    if not check_group:
        logger.warning(f"Group with id '{group_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Group with id '{group_id}' is absent"
        )
    repo_users = UserRepository(session=db)
    check_user = await repo_users.get_one_or_none(User.id == data.creator_id)
    if not check_user:
        logger.warning(f"User-creator with id '{data.creator_id}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"User-creator with id '{data.creator_id}' not found"
        )
    check_group_name = await repo.get_one_or_none(Group.name_group == data.name_group)
    if check_group_name:
        logger.warning(f"Group with name '{data.name_group}' already exist")
        raise HTTPException(
            status_code=403,
            detail=f"Group with name '{data.name_group}' already exist"
        )

    users = []
    for user_id in data.user_ids:
        check_user = await repo_users.get_one_or_none(User.id == user_id)
        if not check_user:
            logger.warning(f"User-participant with id '{user_id}' not found")
            raise HTTPException(
                status_code=404,
                detail=f"User-participant with id '{user_id}' not found"
            )
        users.append(check_user)

    check_group.name_group=data.name_group
    check_group.creator_id=data.creator_id
    check_group.users=users

    logger.info("Update group to repo")
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
    logger.info("Incoming to get groups func")
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
    logger.info("Incoming to get group func")
    repo = GroupRepository(session=db)
    get_group = await repo.get_one_or_none(Group.id == group_id)
    if not get_group:
        logger.warning(f"Group with id '{group_id}' not found")
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