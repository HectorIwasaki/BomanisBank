import sys

def start() -> None: 
    from version_one.database import Database
    print(Database.load_database()) 
    display_welcome_menu()

def display_welcome_menu() -> None:
    from version_one.database import Database
    from version_one.user_services import UserServices
    import version_one.main_menu as main_menu

    while True:
        print('\nWELCOME TO BOMANIS BANK\n')
        print('1. Login')
        print('2. Register')
        print('3. Close Bomanis Bank')
        choice = int(input('Choice: '))
        if choice == 1 or choice == 2 or choice == 3:
            match choice:
                case 1: 
                    print('\nLOGIN:')
                    # checks for correct login information, starts main menu
                    user_id = UserServices.check_for_user()
                    if user_id =='0':
                        continue                    
                    print(main_menu.display_main_menu(Database.user_database[user_id]))                                
                case 2:
                    print('\nREGISTER:')
                    print(UserServices.get_user_information())
                    print(Database.save_database())
                    continue
                case 3:
                    print(Database.save_database())
                    sys.exit('Goodbye...')
                    break
                case _:
                    print('Input was invalid')
                    continue

def main() -> None:   
    start()

if __name__== '__main__':
    main()