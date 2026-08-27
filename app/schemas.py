from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.enums import CurrencyEnum


class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=50)
    amount: Decimal
    description: str | None = Field(default=None, max_length=200)

    @field_validator("amount")
    def validate_amount(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value

    @field_validator("wallet_name")
    def validate_wallet_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Wallet name can't be empty")
        return value


class CreateWalletRequest(BaseModel):
    wallet_name: str = Field(..., max_length=50)
    initial_balance: Decimal = Decimal(0)
    currency: CurrencyEnum = CurrencyEnum.RUB

    @field_validator("wallet_name")
    def validate_wallet_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Wallet name can't be empty")
        return value

    @field_validator("initial_balance")
    def validate_initial_balance(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("Balance must be positive")
        return value


class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)


class UserResponse(UserRequest):
    model_config = {"from_attributes": True}
    id: int


class WalletResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    balance: Decimal
    currency: CurrencyEnum


class OperationResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    wallet_id: int
    type: str
    amount: Decimal
    currency: CurrencyEnum
    category: str | None
    subcategory: str | None
    created_at: datetime


class TransferCreateSchema(BaseModel):
    from_wallet_id: int
    to_wallet_id: int
    amount: Decimal

    @field_validator("to_wallet_id")
    @classmethod
    def wallets_must_differ(cls, v: int, info) -> int:
        if "from_wallet_id" in info.data and v == info.data["from_wallet_id"]:
            raise ValueError("Same wallets id's")
        return v

    @field_validator("amount")
    @classmethod
    def amount_gt_zero(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Amount cannot be negative")
        return v


class TotalBalance(BaseModel):
    total_balance: Decimal
