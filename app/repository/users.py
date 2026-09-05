from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def create_user(db: AsyncSession, login: str) -> User:
    user = User(login=login)
    db.add(user)
    await db.flush()
    return user


async def get_user(db: AsyncSession, login: str) -> User | None:
    query = select(User).where(User.login == login)
    result = await db.execute(query)
    return result.scalar_one_or_none()
