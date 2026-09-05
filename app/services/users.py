from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repository import users as users_repository
from app.schemas import UserResponse


async def create_user(db: AsyncSession, login: str) -> User | None:
    if await users_repository.get_user(db, login):
        raise HTTPException(status_code=400, detail="User already exists")
    user = await users_repository.create_user(db, login)
    return UserResponse.model_validate(user)
