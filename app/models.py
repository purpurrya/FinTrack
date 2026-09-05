from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, def_none_an, pk_an, unique_str_an
from app.enums import CurrencyEnum


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[pk_an]
    name: Mapped[str]
    balance: Mapped[Decimal]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    currency: Mapped[CurrencyEnum] = mapped_column(default=CurrencyEnum.RUB)


class User(Base):
    __tablename__ = "user"

    id: Mapped[pk_an]
    login: Mapped[unique_str_an]


class Operation(Base):
    __tablename__ = "operation"

    id: Mapped[pk_an]
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallet.id"))
    type: Mapped[str]
    amount: Mapped[Decimal]
    currency: Mapped[CurrencyEnum]
    category: Mapped[def_none_an]
    subcategory: Mapped[def_none_an]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())
