from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Wallet


def is_wallet_exists(db: Session, user_id: int, wallet_name: str) -> bool:
    return (
        db.query(Wallet)
        .filter(Wallet.name == wallet_name, Wallet.user_id == user_id)
        .first()
        is not None
    )


def add_income(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = (
        db.query(Wallet)
        .filter(Wallet.name == wallet_name, Wallet.user_id == user_id)
        .first()
    )
    wallet.balance += amount
    db.commit()
    db.refresh(wallet)
    return wallet


def add_expense(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = (
        db.query(Wallet)
        .filter(Wallet.name == wallet_name, Wallet.user_id == user_id)
        .first()
    )
    wallet.balance -= amount
    db.commit()
    db.refresh(wallet)
    return wallet


def get_wallet_by_name(db: Session, user_id: int, wallet_name: str) -> Wallet:
    return (
        db.query(Wallet)
        .filter(Wallet.name == wallet_name, Wallet.user_id == user_id)
        .first()
    )


def get_wallet_balance_by_name(db: Session, user_id: int, wallet_name: str) -> Decimal:
    wallet = (
        db.query(Wallet)
        .filter(Wallet.name == wallet_name, Wallet.user_id == user_id)
        .first()
    )
    return wallet.balance


def get_all_wallets(db: Session, user_id: int) -> list[Wallet]:
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()


def create_wallet(
    db: Session, user_id: int, wallet_name: str, amount: Decimal, currency: str
) -> Wallet:
    wallet = Wallet(
        name=wallet_name, balance=amount, user_id=user_id, currency=currency
    )
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet


def get_wallet_by_id(db: Session, user_id: int, wallet_id: int) -> Wallet | None:
    return (
        db.query(Wallet)
        .filter(Wallet.id == wallet_id, Wallet.user_id == user_id)
        .scalar()
    )
