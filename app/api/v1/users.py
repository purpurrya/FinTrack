from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas import UserRequest, UserResponse
from app.services import users as users_service

router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create_user(payload: UserRequest, db: AsyncSession = Depends(get_db)):
    return await users_service.create_user(db, payload.login)


@router.get("/users/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
