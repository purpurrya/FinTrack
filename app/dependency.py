from collections.abc import Generator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.cache.redis import cache
from app.config import settings
from app.database import SessionLocal
from app.models import User
from app.repository import users as users_repository

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _user_cache_key(login: str) -> str:
    return f"user:{login}"


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    login = credentials.credentials
    key = _user_cache_key(login)

    cached_user = await cache.get(key)
    if cached_user:
        return User(**cached_user)

    user = users_repository.get_user(db, login)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await cache.set(
        key,
        {"id": user.id, "login": user.login},
        ttl_seconds=settings.cache_ttl_seconds,
    )
    return user
