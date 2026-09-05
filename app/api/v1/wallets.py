from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas import CreateWalletRequest, TotalBalance, WalletResponse
from app.services import wallets as wallets_service

router = APIRouter()


@router.get("/balance", response_model=TotalBalance)
async def get_balance(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await wallets_service.get_balance(db, current_user)


@router.post("/wallets", response_model=WalletResponse)
async def create_wallet(
    wallet: CreateWalletRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await wallets_service.create_wallet(db, current_user, wallet)


@router.get("/wallets", response_model=list[WalletResponse])
async def get_all_wallets(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await wallets_service.get_all_wallets(db, current_user)
