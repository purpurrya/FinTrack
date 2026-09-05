from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

from app.config import settings

connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)
engine = create_async_engine(settings.database_url, connect_args=connect_args)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


def_none_an = Annotated[str | None, mapped_column(default=None)]

pk_an = Annotated[int, mapped_column(primary_key=True)]

unique_str_an = Annotated[str, mapped_column(unique=True)]
