from random import randint
from typing import TYPE_CHECKING
from enum import StrEnum
from transaction import TransactionHistory

if TYPE_CHECKING:
    from account_library import AccountLibrary

class AccountType(StrEnum):
    CHECKINGS = 'Checkings Account'
    SAVINGS = 'Savings Account'

class BankAccount():
    
    def __init__(self, account_type: AccountType, balance: float = 0) -> None:
        self.account_type = account_type
        self.balance = balance
        self.account_number = str(randint(0,999999))
        self.transaction_history = TransactionHistory() #list of transactions made on the account
    
    def __str__(self):
        return f'''Account type:{self.account_type}\
        Account number:{self.account_number}\
        Account balance: ${self.balance:,.2f}'''
           
    @property
    def account_type(self) -> str:
        return self._account_type
    
    @account_type.setter
    def account_type(self, account_type: str):
        if account_type not in (AccountType.CHECKINGS, AccountType.SAVINGS):
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

    @classmethod
    def make_account(cls, account_library: 'AccountLibrary', account_type: AccountType) -> str:
        print(f'\nThank you for choosing to open a {account_type} with Bomanis Bank. ')
        #CHECK FOR INVALID INPUT
        starting_balance = float(input('How much would you like to deposit for your starting balance?' + 
                                                '\nor enter "0" to go back to the main menu: '))
        if starting_balance == 0:
            return f'Now being directed to the main menu...'
        account = BankAccount(account_type, starting_balance)
        account_library.add_account(account.account_number, account)
        return f'\nYou deposited ${account.balance:,.2f} into your new {account_type}.\n' + \
                f'Your checkings account number is: {account.account_number}\n'  + \
                f'You will now be directed back to the main menu...'
    
    @staticmethod
    def get_account_statement(sending_account: 'BankAccount', recieving_account: 'BankAccount') -> str:
        return(f'\nThe balance in your sending [{sending_account.account_type}: ' +
            f'{sending_account.account_number}] is: ' +
            f'${sending_account.balance:,.2f}' +                    
            f'\nThe balance in your recieving [{recieving_account.account_type}: ' +
            f'{recieving_account.account_number}] is: ' +
            f'${recieving_account.balance:,.2f}')