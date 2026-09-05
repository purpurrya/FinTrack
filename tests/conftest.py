from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.dependency import get_db
from app.models import User, Wallet
from main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestAsyncSessionLocal = async_sessionmaker(
    test_engine, expire_on_commit=False, autoflush=False
)


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as db:
        yield db


app.dependency_overrides[get_db] = get_test_db


@pytest_asyncio.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as db:
        yield db


@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> User:
    user = User(login="test")
    db_session.add(user)
    await db_session.commit()
    return user


@pytest_asyncio.fixture
async def make_wallet(db_session: AsyncSession, user: User):
    async def _make(name="card", balance=100):
        wallet = Wallet(name=name, balance=balance, user_id=user.id)
        db_session.add(wallet)
        await db_session.commit()
        return wallet

    return _make


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
