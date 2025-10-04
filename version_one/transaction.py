from enum import StrEnum
from datetime import datetime
   
class TransactionHistory:
    
    def __init__(self) -> None:      
        self.transaction_history: list[Transaction] = [] 

    def __str__(self) -> str:
        if not self.transaction_history:
            return 'No transactions have been made yet.'
        return '\n'.join(str(transaction) for transaction in self.transaction_history)
    
    def add_transaction(self, transaction: 'Transaction') -> None:
        self.transaction_history.append(transaction)
        
class TransactionType(StrEnum):
    DEPOSIT = 'Deposit'
    WITHDRAW = 'Withdraw'
    TRANSFER = 'Transfer'

class Transaction:

    def __init__(self, transaction_type: TransactionType, amount: float) -> None:
        self.transaction_type = transaction_type
        self.amount = amount
        self._timestamp = datetime.now()

    def __str__(self) -> str:
        return f'Transaction Type: {self.transaction_type}, Amount: ${self._amount:,.2f}, Date: {self._timestamp.strftime("%Y-%m-%d %H:%M:%S")}\n'

    @property
    def transaction_type(self) -> str:
        return self._transaction_type
    
    @transaction_type.setter
    def transaction_type(self, transaction_type: str) -> None:
        if transaction_type in TransactionType:
            self._transaction_type = transaction_type
        else:
            raise ValueError(f'{transaction_type} is not a valid transaction type')
    
    #is getter and setter for amount necessary?   
    @property
    def amount(self) -> float:
        return self._amount
    
    @amount.setter
    def amount(self, amount: float) -> None:
        if amount < 0:
            raise ValueError('Cannot be a negative number')
        self._amount = amount
        
    @property
    def timestamp(self) -> datetime:
        return self._timestamp
         