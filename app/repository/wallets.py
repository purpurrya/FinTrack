from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Wallet


async def is_wallet_exists(db: AsyncSession, user_id: int, wallet_name: str) -> bool:
    result = await db.execute(
        select(Wallet).where(Wallet.name == wallet_name, Wallet.user_id == user_id)
    )
    return result.scalar_one_or_none() is not None


async def add_income(
    db: AsyncSession, user_id: int, wallet_name: str, amount: Decimal
) -> Wallet:
    result = await db.execute(
        select(Wallet).where(Wallet.name == wallet_name, Wallet.user_id == user_id)
    )
    wallet = result.scalar_one_or_none()
    wallet.balance += amount
    await db.flush()
    return wallet


async def add_expense(
    db: AsyncSession, user_id: int, wallet_name: str, amount: Decimal
) -> Wallet:
    result = await db.execute(
        select(Wallet).where(Wallet.name == wallet_name, Wallet.user_id == user_id)
    )
    wallet = result.scalar_one_or_none()
    wallet.balance -= amount
    await db.flush()
    return wallet


async def get_wallet_by_name(
    db: AsyncSession, user_id: int, wallet_name: str
) -> Wallet | None:
    result = await db.execute(
        select(Wallet).where(Wallet.name == wallet_name, Wallet.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_wallet_balance_by_name(
    db: AsyncSession, user_id: int, wallet_name: str
) -> Decimal:
    wallet = await get_wallet_by_name(db, user_id, wallet_name)
    return wallet.balance


async def get_all_wallets(db: AsyncSession, user_id: int) -> list[Wallet]:
    result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
    return list(result.scalars().all())


async def create_wallet(
    db: AsyncSession, user_id: int, wallet_name: str, amount: Decimal, currency: str
) -> Wallet:
    wallet = Wallet(
        name=wallet_name, balance=amount, user_id=user_id, currency=currency
    )
    db.add(wallet)
    await db.flush()
    return wallet


async def get_wallet_by_id(
    db: AsyncSession, user_id: int, wallet_id: int
) -> Wallet | None:
    result = await db.execute(
        select(Wallet).where(Wallet.id == wallet_id, Wallet.user_id == user_id)
    )
    return result.scalar_one_or_none()
