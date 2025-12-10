import sqlite3
from db import get_db_connection
from bank_account import BankAccount

class BankAccountServices:
    """Service layer for bank account operations. Handles database interactions."""
    @staticmethod
    def get_account_by_id(account_id: int) -> BankAccount | None:
        """Fetches a bank account by its ID from the database."""
        db = get_db_connection()
        row = db.execute("SELECT * FROM bank_accounts WHERE id = ?", (account_id,)).fetchone()
        db.close()
        return BankAccount.from_row(row)
        
    @staticmethod
    def get_account_for_user(account_id: int, user_id: int) -> BankAccount:
        """Fetches a bank account by its ID and ensures it belongs to the specified user."""
        bank_account = BankAccountServices.get_account_by_id(account_id)
        if bank_account is None:
            raise ValueError("Account not found")
        if bank_account.user_id != user_id:
            raise PermissionError("Do not have access to this account")
        return bank_account
    
    @staticmethod
    def update_account_balance(account_id: int | None, new_balance: float, db: sqlite3.Connection ) -> None:
        """Updates the balance of a bank account in the database."""
        db.execute(
            "UPDATE bank_accounts SET balance = ? WHERE id = ?",
            (new_balance, account_id)
        )
        db.commit()