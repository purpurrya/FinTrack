from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas import OperationRequest, OperationResponse, TransferCreateSchema
from app.services import operations as operations_service

router = APIRouter()


@router.post("/operations/income", response_model=OperationResponse)
async def add_income(
    operation: OperationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await operations_service.add_income(db, current_user, operation)


@router.post("/operations/expense", response_model=OperationResponse)
async def add_expense(
    operation: OperationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await operations_service.add_expense(db, current_user, operation)


@router.get("/operations", response_model=list[OperationResponse])
async def get_operation_list(
    wallet_id: int | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await operations_service.get_operations_list(
        db, current_user, wallet_id, date_from, date_to
    )


@router.post("/operations/transfer", response_model=OperationResponse)
async def create_transfer(
    payload: TransferCreateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await operations_service.transfer_between_wallets(
        db,
        current_user.id,
        payload.from_wallet_id,
        payload.to_wallet_id,
        payload.amount,
    )
