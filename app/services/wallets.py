from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import CurrencyEnum
from app.models import User
from app.repository import wallets as wallet_repository
from app.schemas import CreateWalletRequest, TotalBalance, WalletResponse
from app.services import exchange_service


async def get_balance(db: AsyncSession, current_user: User) -> TotalBalance:
    wallets = await wallet_repository.get_all_wallets(
        db,
        current_user.id,
    )
    total_balance = Decimal(0)
    for wallet in wallets:
        if wallet.currency == CurrencyEnum.RUB:
            total_balance += wallet.balance
        else:
            exchange_rate = await exchange_service.get_exchange_rate(
                wallet.currency, CurrencyEnum.RUB
            )
            total_balance += exchange_rate * wallet.balance
    return TotalBalance(total_balance=total_balance)


async def create_wallet(
    db: AsyncSession, current_user: User, wallet: CreateWalletRequest
) -> WalletResponse:
    if await wallet_repository.is_wallet_exists(
        db, current_user.id, wallet.wallet_name
    ):
        raise HTTPException(status_code=400, detail="Wallet already exists")
    created_wallet = await wallet_repository.create_wallet(
        db, current_user.id, wallet.wallet_name, wallet.initial_balance, wallet.currency
    )
    return WalletResponse.model_validate(created_wallet)


async def get_all_wallets(db: AsyncSession, current_user: User) -> list[WalletResponse]:
    wallets = await wallet_repository.get_all_wallets(db, current_user.id)
    return [WalletResponse.model_validate(wallet) for wallet in wallets]
