from enum import StrEnum

class TransactionType(StrEnum):
    """Defines types of transactions."""
    DEPOSIT = 'deposit' # Future use
    WITHDRAW = 'withdrawal' # Future use
    TRANSFER = 'transfer'
