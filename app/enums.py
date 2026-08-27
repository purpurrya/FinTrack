from enum import StrEnum, auto


class CurrencyEnum(StrEnum):
    RUB = auto()
    USD = auto()
    EUR = auto()


class OperationEnum(StrEnum):
    EXPENSE = auto()
    INCOME = auto()
    TRANSFER = auto()
