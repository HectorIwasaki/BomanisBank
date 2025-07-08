from user import User
from bank_account import BankAccount

class UserServices:
    
    @staticmethod
    def get_user_information()  -> str:
        from database import Database
        print('Please answer the follwing questions:...')
        first_name = input('What is your first name?:')
        last_name = input('What is your last name?:')
        birthday = input('What is your birthday as yyyy-mm-dd:')
        pin = input('Please create a 4 digit pin:')
        return Database.add_user_to_database(User(first_name, last_name, birthday, pin))
        
    @staticmethod
    def delete_user(user: 'User') -> str:
        from database import Database
        while True:
            print('\n!!!ACCOUNT DELETION!!!')
            print('Are you sure you want to delete your account? (y/n)')
            confirmation = input('Please enter y or n: ')
            if confirmation.lower() == 'y':
                break
            elif confirmation.lower() == 'n':
                print('Account deletion cancelled.')
                return 'Now returning to the main menu...'
            else:
                print('Invalid input. Please enter y or n.')
                continue
        print(f'Hope to see you again {user.user_id}...')
        print('Deleting account...')
        del Database.user_database[user.user_id]
        return 'Account deleted'
        
        
    @staticmethod
    def check_for_user() -> str:
        from database import Database
        while True:
            user_id = input('Please enter your User ID or '+
                            'enter "0" to return:')
            if user_id == '0':
                print('Now returning')
                return user_id
            elif user_id in Database.user_database:
                print(f'Welcome back {user_id}')      
                while True:
                    entered_pin = input('Please enter your pin or '+
                                        'enter "0" to return:')
                    if entered_pin == '0':
                        return entered_pin
                    elif entered_pin == Database.user_database[user_id].pin:
                        return user_id
                    else:
                        print (f'{entered_pin} is the incorrect password')
                        continue
            else:
                print(f'{user_id} not found')
                continue              
        
        

    @staticmethod
    def check_for_bank_account(user: 'User') -> BankAccount:
        while True:
            account_number = input('Account Number: ')                                    
            if bank_account := user.checkings_library.get_account(account_number):
                return bank_account                           
            elif bank_account := user.savings_library.get_account(account_number):
                return bank_account
            else:
                print(f'{account_number} is an invalid account number')
                continue