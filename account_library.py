from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bank_account import BankAccount
    
class AccountLibrary:

    def __init__(self) -> None:
        self.library : dict[str ,'BankAccount'] = {} # key = account_number, value = BankAccount

    def add_account(self, account_number: str, account: "BankAccount") -> None: 
        if account_number in self.library:
            raise ValueError(f'Account {account_number} already exists.')
        self.library[account_number] = account
    
    def remove_account(self, account_number: str) -> None:
        if account_number not in self.library:
            raise ValueError(f'Account {account_number} does not exist.')
        del self.library[account_number]

    def get_account(self, account_number: str) -> 'BankAccount':
        if account_number not in self.library:
            raise ValueError(f'Account {account_number} does not exist.')
        return self.library[account_number]
    
    def get_all_accounts(self) -> list['BankAccount']:
        return list(self.library.values())
    
    def get_all_account_numbers(self) -> list[str]:
        return list(self.library.keys())
    
    def display_accounts(self) -> str:
        if not self.library:
            return '\nNo accounts available.'
        return '\n'.join(f'\n{account.account_type}: {acc_num}        ${account.balance:,.2f}'
                         for acc_num, account in self.library.items())
    
    
    