from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.database import get_db
# from app.schemas.user import UserResponse, UserCreate, UserLogin, RefreshToken
# from app.services.auth_service import reg_user, login_user, refresh_my_token

router = APIRouter()


@router.post('/group')#, response_model=UserResponse)
async def create_group(): #user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    # result = await reg_user(user, db)
    # return result
    pass


@router.delete('/group/{int: id}')
async def delete_group(id: int):
    pass


@router.put('/group/{int: id}')
async def change_group(id: int):
    pass


@router.get('/group')
async def get_groups():
    pass


@router.get('/group/{int: id}')
async def get_group(id: int):
    pass