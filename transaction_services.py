from transaction import Transaction, TransactionType
from bank_account import BankAccount
from user_services import UserServices
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from user import User

class TransactionServices:
     
    @staticmethod
    def deposit(user) -> str:
        #User chooses an account
        bank_account: BankAccount = UserServices.check_for_bank_account(user) 
        print(f'\nYour current balance in this account is: ${bank_account.balance:,.2f}')
        while True:
            try:
                amount = int(input('Please enter the amount you would like to deposit or' +
                                   'enter "0" to return:'))
                if amount == 0:
                    return 'Now returning'                    
                if amount < 0:
                    print(f'{amount} is not valid amount.')
                    continue
                print(f'Now depositing ${amount:,.2f}...')
                bank_account._balance += amount
                bank_account.transaction_history.add_transaction(Transaction(TransactionType.DEPOSIT, amount))
                return f'Your new balance is: ${bank_account.balance:,.2f}\n' + \
                    f'Now being directed back to the main menu...'    
            except ValueError:
                print('Please enter a valid amount.')
                continue      
             
    @staticmethod   
    def withdraw(user) -> str:
        #User chooses an account
        bank_account: BankAccount = UserServices.check_for_bank_account(user)       
        print(f'Your current balance in this account is: ${bank_account.balance:,.2f}')
        while True:
            try:
                amount = int(input('Please enter the amount you would like to withdraw or '+
                                   'enter "0" to return:'))
                if amount == 0:
                    return 'Now returning'
                if amount > bank_account.balance:
                    print(f'{amount:,.2f} exceeds the balance in your account.')
                    continue                           
                print(f'Now withdrawing ${amount:,.2f}')                        
                bank_account._balance -= amount
                bank_account.transaction_history.add_transaction(Transaction(TransactionType.WITHDRAW, amount))                            
                return f'Your new balance is: ${bank_account.balance:,.2f}' + \
                    f'\nNow being directed back to the main menu...'
            except ValueError:
                print(f'{amount} is not a valid amount.')
                continue
           
    @staticmethod
    def transfer(sending_account: 'BankAccount', recieving_account: 'BankAccount') -> str | None:
        while True:
            try:
                amount = int(input('\nPlease enter the amount you would like to transfer or' + 
                                    'enter "0" to return:'))
                if amount == 0:
                    return 'Now being directed to the main menu...'
                sending_account._balance -= amount
                recieving_account._balance += amount
                sending_account.transaction_history.add_transaction(Transaction(TransactionType.TRANSFER, amount))
                recieving_account.transaction_history.add_transaction(Transaction(TransactionType.TRANSFER, amount))
                print('\nTransfer completed successfully:')
                print(BankAccount.get_account_statement(sending_account, recieving_account))
                return 'Now returning to main menu'
            except ValueError:
                print(f'{amount} is not a valid amount.')
                continue
            
    @staticmethod
    def get_transfer_combination(user: 'User') -> str | None:   
        #calls the transfer function   
        sending_account = input('\nWhich account number are you transfering from'+
                                'enter 0 to return:')
        if sending_account == '0':
            return 'Now returning'
        recieving_account = input('\nWhich account number are your transfering to'+
                                  'enter "0" to return')
        if recieving_account =='0': 
            return 'Now returning'

        #finds which account is in which library as a combination
        #both accounts are in checkings library  #COMBINATION 1
        if sending_account in user.checkings_library.get_all_account_numbers() and recieving_account in user.checkings_library.get_all_account_numbers():
            print(BankAccount.get_account_statement(user.checkings_library.get_account(sending_account), user.checkings_library.get_account(recieving_account)))
            return TransactionServices.transfer(user.checkings_library.get_account(sending_account), user.checkings_library.get_account(recieving_account))
                 
        #both accounts are in savings library  #COMBINATION 2
        elif sending_account in user.savings_library.get_all_account_numbers() and recieving_account in user.savings_library.get_all_account_numbers():               
            print(BankAccount.get_account_statement(user.savings_library.get_account(sending_account), user.savings_library.get_account(recieving_account)))
            return TransactionServices.transfer(user.savings_library.get_account(sending_account), user.savings_library.get_account(recieving_account)) 
                                                  
        #sending account is in checkings library AND receiving account is in savings library #COMBINATION 3
        elif sending_account in user.checkings_library.get_all_account_numbers() and recieving_account in user.savings_library.get_all_account_numbers():                                               
            print(BankAccount.get_account_statement(user.checkings_library.get_account(sending_account), user.savings_library.get_account(recieving_account)))
            return TransactionServices.transfer(user.checkings_library.get_account(sending_account), user.savings_library.get_account(recieving_account))
                             
        #sending account is in savings library AND recieving account is in checkings library  #COMBINATION 4 
        elif sending_account in user.savings_library.get_all_account_numbers() and recieving_account in user.checkings_library.get_all_account_numbers():                                               
            print(BankAccount.get_account_statement(user.savings_library.get_account(sending_account), user.checkings_library.get_account(recieving_account)))
            return TransactionServices.transfer(user.savings_library.get_account(sending_account), user.checkings_library.get_account(recieving_account))
        else:
            return 'One or both of those accounts do not exist...'