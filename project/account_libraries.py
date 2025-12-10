from __future__ import annotations # So forward references work in type hints within the class
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bank_account import BankAccount

class LibraryType(StrEnum):
    """Enumeration for different types of account libraries."""
    CHECKING = 'checking'
    SAVINGS = 'savings'
    
class AccountLibraries:
    """Manages a collection of bank accounts for a user based on account type.
    Domain layer for managing account libraries in memory"""
    def __init__(self, id: int | None, user_id: int, library_type: LibraryType) -> None:
        self.id = id # type: ignore
        self.user_id = user_id
        self.library_type = library_type
        self.accounts: dict[str, 'BankAccount'] = {}  # Key: account_number,  Value: BankAccount instances

    def add_account(self, account_number: str, bank_account: 'BankAccount') -> None:
        """Adds a new account to the library."""
        self.accounts[account_number] = bank_account

    def get_account(self, account_number: str) -> BankAccount | None:
        """Retrieves an account by its account number."""
        return self.accounts.get(account_number)
    
    def remove_account(self, account_number: str) -> None:
        """Removes an account from the library."""
        self.accounts.pop(account_number, None)
    
    def all_accounts(self) -> list['BankAccount']:
        """Returns a list of all accounts in the library."""
        return list(self.accounts.values())
    
    def total_balance(self) -> float:
        """Calculates the total balance of all accounts in the library."""
        return sum(account.balance for account in self.accounts.values())

    @property
    def id(self) -> None:
        return self._id
    
    @id.setter
    def id(self, id: None) -> None:
        self._id = id

    @property
    def user_id(self) -> int:
        return self._user_id
    
    @user_id.setter
    def user_id(self, user_id: int) -> None:
        if user_id <= 0:
            raise ValueError(f'{user_id} is not a valid user ID')
        self._user_id = user_id

    @property
    def library_type(self) -> LibraryType:
        return self._library_type
    
    @library_type.setter
    def library_type(self, library_type: LibraryType) -> None:
        if library_type not in (LibraryType.CHECKING, LibraryType.SAVINGS):
            raise ValueError(f'{library_type} is not a valid library type')
        self._library_type = library_type

        
        


    
    