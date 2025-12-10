from random import randint
from enum import StrEnum
import re
from db import get_db_connection


class AccountType(StrEnum):
    CHECKING = 'checking'
    SAVINGS = 'savings'


class BankAccount:
    """Represents a bank account.
    Domain layer for bank account objects."""
    def __init__(self, id: int | None, user_id: int, account_type: AccountType, balance: float = 0, nickname: str = "", debit_card: str = "no", account_number: str | None = None) -> None:
        self.id = id
        self.user_id = user_id
        # allow callers to pass either an AccountType or a string
        self.account_type = account_type
        self.balance = balance
        self.nickname = nickname
        self.debit_card = debit_card
        # preserve existing account_number if provided, otherwise generate a new unique one
        if account_number is None:
            self.account_number = self.generate_account_number
        else:
            self.account_number = account_number

    def __str__(self):
        return f"""Account type:{self.account_type.value}\
        Account number:{self.account_number}\
        Account balance: ${self.balance:,.2f}\
        Account nickname: {self.nickname}\
        Debit card: {self.debit_card}"""

    @classmethod
    def from_row(cls, row):
        """Constructs a BankAccount domain object from a DB row/dict."""
        if row is None:
            return None
        # row is expected to support mapping access (sqlite3.Row)
        return cls(
            id=row['id'] if not isinstance(row, dict) else row.get('id'),
            user_id=row['user_id'] if not isinstance(row, dict) else row.get('user_id'), # type: ignore
            account_type=row['account_type'] if not isinstance(row, dict) else row.get('account_type'), # type: ignore
            balance=row['balance'] if not isinstance(row, dict) else row.get('balance'), # type: ignore
            nickname=row['nickname'] if not isinstance(row, dict) else row.get('nickname'), # type: ignore
            debit_card=row['debit_card'] if not isinstance(row, dict) else row.get('debit_card'), # type: ignore
            account_number=row['account_number'] if not isinstance(row, dict) else row.get('account_number'),
        )

    def save_bank_account(self, db) -> None:
        """Saves the bank account to the database."""
        cursor = db.execute(
            "INSERT INTO bank_accounts (user_id, account_type, balance, nickname, debit_card, account_number) VALUES (?, ?, ?, ?, ?, ?)",
            (self.user_id, self.account_type.value, self.balance, self.nickname, self.debit_card, self.account_number)
        )
        db.commit()
        self.id = cursor.lastrowid

    @property
    def account_type(self) -> AccountType:
        return self._account_type

    @account_type.setter
    def account_type(self, account_type):
        """Accept either an AccountType or a string and normalize to AccountType."""
        # convert from raw string if necessary
        if isinstance(account_type, str):
            try:
                account_type = AccountType(account_type)
            except ValueError:
                raise ValueError(f'{account_type} is not a valid account type')

        if account_type not in (AccountType.CHECKING, AccountType.SAVINGS):
            raise ValueError(f'{account_type} is not a valid account type')
        self._account_type = account_type

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, balance: float):
        if balance < 0:
            raise ValueError(f'{balance} is not a valid number')
        else:
            self._balance = balance

    @property
    def nickname(self) -> str:
        return self._nickname

    @nickname.setter
    def nickname(self, nickname: str) -> None:
        """Length between 1 and 50 characters
        Contains only letters, spaces, hyphens, or apostrophes
        """
        if nickname is None:
            raise ValueError('Nickname cannot be None')
        if not (1 <= len(nickname) <= 50):
            raise ValueError('Nickname must be between 1 and 50 characters long')
        if not re.match(r"^[a-zA-Z\s'-]+$", nickname):
            raise ValueError(f'{nickname} is not a Nickname')
        self._nickname = nickname

    @property
    def debit_card(self) -> str:
        return self._debit_card

    @debit_card.setter
    def debit_card(self, debit_card: str) -> None:
        if debit_card not in ("yes", "no"):
            raise ValueError(f'{debit_card} is not a valid option')
        self._debit_card = debit_card

    @property
    def generate_account_number(self) -> str:
        """Generates a Unique random 6 digit account number"""
        while True:
            account_number = f"{randint(0, 999999):06}" # Generate a random 6-digit number with leading zeros
            db = get_db_connection()
            existing_account = db.execute("SELECT * FROM bank_accounts WHERE account_number = ?", (account_number,)).fetchone()
            if existing_account is None:
                return account_number
        