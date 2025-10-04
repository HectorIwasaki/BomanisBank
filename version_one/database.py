import pickle
bomanis_bank_users = 'bomanis_bank_users.pickle'

class Database:
    from user import User
    
    user_database: dict[str, User] = {}

    @classmethod
    def add_user_to_database(cls, user: User) -> str:
        cls.user_database[user.user_id] = user
        print(f'\nWelcome {user.first_name} {user.last_name}...')
        print(f'Your userID is {user.user_id}') 
        print(f'Your 4 digit pin is: {user.pin}')
        return 'Now returning to main menu.'

    @classmethod
    def save_database(cls) -> str:
        try:
            with open(bomanis_bank_users, 'wb') as file:
                pickle.dump(cls.user_database, file)
                return f'Database saved successfully.'
        except Exception as error:
            print(f'An error occurred while saving the database: {error}')
            return 'Failed to save the database.'
    
    @classmethod
    def load_database(cls) -> str:
        try: 
            with open(bomanis_bank_users, 'rb') as file:
                cls.user_database = pickle.load(file)
                return f'Successfully loaded database with {len(cls.user_database)} entries'
        except Exception as error:
            return f'An error occurred while loading the database: {error}'

    @classmethod
    def delete_database(cls) -> str:
        try:
            with open(bomanis_bank_users, 'wb') as file:
                cls.user_database = {}
                pickle.dump(cls.user_database, file)
                return f'Database deleted successfully.'
        except Exception as error:
            print(f'An error occurred while deleting the database: {error}')
            return 'Failed to delete the database.'         