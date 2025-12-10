import sqlite3
from datetime import datetime

class TransactionServices:
    """Service layer for transaction operations. Handles database interactions."""
    @staticmethod
    def record_transaction(account_id: int | None, recipient_account_id: int | None, amount: float, transaction_type: str, db: sqlite3.Connection) -> None:
        """Records a transaction in the database."""
        now = datetime.now()
        # Exclude seconds for consistency
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M")
        db.execute(
            "INSERT INTO transactions (account_id, recipient_account_id, amount, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?)",
            (account_id,recipient_account_id, amount, transaction_type, formatted_datetime))
        
        db.commit()