from user import User
from user_services import UserServices


def display_main_menu(user: User) -> None:
    from bank_account import BankAccount, AccountType
    from database import Database
    from welcome_menu import display_welcome_menu
    from transaction_services import TransactionServices
    from account_library import AccountLibrary
    
    choice = 0
    while True:
        print('\nBOMANIS BANK MAIN MENU')
        print(AccountLibrary.display_accounts(user.checkings_library))  
        print(AccountLibrary.display_accounts(user.savings_library))
        print('\n1.Open an account | 2.Make a deposit | 3.Make a withdraw | 4.Make a transfer | 5.View Profile | 6.Log out of Bomanis Bank')
      
        choice = int(input('Choice: '))
        match choice:     
            case 1:
                print('\nOPEN AN ACCOUNT:')
                print('1.Open a Checkings Account')
                print('2.Open a Savings Account')
                print('3.Main Menu')           
                try:
                    choice = int(input('\nChoice:'))
                    while(choice != 3):
                        match choice:
                            case 1:
                                print(BankAccount.make_account(user.checkings_library, AccountType.CHECKINGS))
                                print(Database.save_database())
                                break                          
                            case 2:
                                print(BankAccount.make_account(user.savings_library, AccountType.SAVINGS))
                                print(Database.save_database())
                                break
                            case _:
                                print('Invalid input')
                                break
                except ValueError:
                    print('Please enter a valid number')
                    continue
            case 2:
                print('\nDEPOSIT:')
                print('1.Deposit into a Checkings')
                print('2.Deposit into a Savings')
                print('3.Main Menu')
                try:
                    choice = int(input('\nChoice: '))
                    while(choice != 3):
                        match choice:
                            case 1:
                                print('\nChoose a checkings account to deposit to:')
                                print(AccountLibrary.display_accounts(user.checkings_library))
                                print(TransactionServices.deposit(user))
                                print(Database.save_database())
                                break                          
                            case 2:
                                print('\nChoose a savings account to deposit to:')
                                print(AccountLibrary.display_accounts(user.savings_library))
                                print(TransactionServices.deposit(user))
                                print(Database.save_database())
                                break
                            case _:
                                print('Invalid input')
                                break
                except ValueError:
                    print('Please enter a valid number')
                    continue
            case 3:
                print('\nWITHDRAW:')
                print('1.Withdraw from a Checkings')
                print('2.Withdraw from a Savings')
                print('3.Main Menu')    
                choice = int(input('\nChoice: '))
                while(choice != 3):
                    match choice:
                        case 1:
                            print('\nChoose a checkings account to withdraw from:')
                            print(AccountLibrary.display_accounts(user.checkings_library))
                            print(TransactionServices.withdraw(user))
                            print(Database.save_database())
                            break                 
                        case 2:
                            print('\nChoose a savings account to withdraw from:')
                            print(AccountLibrary.display_accounts(user.savings_library))
                            print(TransactionServices.withdraw(user))
                            print(Database.save_database())
                            break                             
                        case _:
                            print('Invalid input')
                            continue
            case 4: 
                #Display the checkings and savings accounts available for transfer
                print('\nAccounts availible to make a transfer:')
                print(AccountLibrary.display_accounts(user.checkings_library))  
                print(AccountLibrary.display_accounts(user.savings_library))                 
                #starts the transfer process
                print(TransactionServices.get_transfer_combination(user))
                print(Database.save_database())               
            case 5:
                print('\nProfile:\n')
                print(user)
                print('\n1.View transaction history | 2.Delete Account | 3.Return to main menu')
                choice = int(input('Choice: '))
                while(choice != 3):
                    match choice:
                        case 1:
                            print('\nAccounts')
                            print('\nChoose an account to view its history, ' +
                            'or enter "0" to return\n')
                            print(AccountLibrary.display_accounts(user.checkings_library))  
                            print(AccountLibrary.display_accounts(user.savings_library))
                            bank_account = UserServices.check_for_bank_account(user)
                            print('\nTRANSACTION HISTORY:')
                            print(bank_account.transaction_history)
                            break              
                        case 2:
                            print(UserServices.delete_user(user))
                            print(Database.save_database())
                            display_welcome_menu()                             
                        case _:
                            print('Invalid input')
                            continue
            case 6:               
                print('Logging out of Bomanis Bank...')
                print(Database.save_database())
                display_welcome_menu()
            case _:
                print('Invalid input')
                continue
                    