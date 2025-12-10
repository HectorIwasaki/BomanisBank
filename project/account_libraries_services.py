from  account_libraries import AccountLibraries, LibraryType
from bank_account import BankAccount, AccountType
import sqlite3

class AccountLibrariesServices:
    """Provides Account Library utilites for creating, loading, and managing account libraries in the database."""
    # Persistence layer for SQLite database

    @staticmethod
    def create_default_libraries(user_id: int | None, db: sqlite3.Connection) -> None:
        for lib_type in (LibraryType.CHECKING, LibraryType.SAVINGS):
            db.execute(
                "INSERT INTO account_libraries (user_id, library_type) VALUES (?, ?)",
                (user_id, lib_type.value)
            )
        db.commit()

    @staticmethod
    def load_from_library(user_id : int, library_type: LibraryType, db: sqlite3.Connection) -> AccountLibraries:
        """Load a users library from the database and its associated accounts."""
        # Get the library ID
        library_id = AccountLibrariesServices.get_library_id(user_id, library_type, db)
        # Create the library instance
        library = AccountLibraries(id=library_id, user_id=user_id, library_type=library_type)

        # Fetch all accounts linked to this library
        query = """
            SELECT account_info.account_number, account_info.balance, account_info.nickname, account_info.id, account_info.account_type, account_info.debit_card
            FROM bank_accounts AS account_info
            INNER JOIN account_mappings AS am ON am.account_id = account_info.id
            WHERE am.library_id = ?
        """
        rows = db.execute(query, (library_id,)).fetchall()

        for row in rows:
            # Preserve the stored account_number when reconstructing the domain object
            bank_account = BankAccount(
                id=row["id"],
                user_id=user_id,
                # normalize stored string to AccountType enum
                account_type=AccountType(row["account_type"]),
                balance=row["balance"],
                nickname=row["nickname"],
                debit_card=row["debit_card"],
                account_number=row["account_number"]
            )
            library.add_account(row["account_number"], bank_account)
        
        return library
        
    @staticmethod
    def add_account_to_library(library_id: int | None, account_id: int | None, db: sqlite3.Connection) -> None:
        """Creates the link between a library and an account in the database."""
        db.execute(
            "INSERT INTO account_mappings (library_id, account_id) VALUES (?, ?)",
            (library_id, account_id)
        )
        db.commit()

    @staticmethod
    def get_library_id(user_id: int, library_type: LibraryType, db: sqlite3.Connection) -> int:
        """Fetches the library ID for a user and library type."""
        row = db.execute(
            "SELECT id FROM account_libraries WHERE user_id = ? AND library_type = ?",
            (user_id, library_type.value)
        ).fetchone()
        if row is None:
            raise ValueError(f'Library of type {library_type} for user ID {user_id} not found.')
        return row["id"]