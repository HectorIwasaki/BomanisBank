from datetime import datetime
from werkzeug.security import generate_password_hash
from db import get_db_connection
import re


class User:
    """Represents a user of BomanisBank.
    Domain layer for managing user data in memory"""
     
    def __init__(self, id: int | None, first_name: str, last_name: str, username: str, date_of_birth: str, password: str) -> None: 
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.date_of_birth = date_of_birth
        self.password_hash = password

    @classmethod
    def from_row(cls, row) -> 'User | None':
        """Constructs a User from a DB values of row/dict
        This bypasses password validation and hashing because the DB already stores a hashed password.
        """
        if row is None:
            return None
        # create instance without running __init__ to avoid re-validation
        user = object.__new__(cls)
        # assign private attributes expected by the class
        user._id = row['id']
        user._first_name = row['first_name']
        user._last_name = row['last_name']
        # store the username directly to avoid uniqueness check in the setter
        user._username = row['username']
        # date_of_birth property stores into _date_of_birth
        user._date_of_birth = row['date_of_birth']
        # set the already-hashed password directly
        user._password_hash = row['password_hash']
        user._created_at = row['created_at']
        return user

    def __str__(self) -> str:
        return f'''Name: {self.first_name} {self.last_name}\
        Date of Birth: {self.date_of_birth}\
        User ID: {self.id}\
        Password: {self.password_hash}'''

    @property
    def id(self) -> int | None:
        return self._id
    
    @id.setter
    def id(self, id: int | None) -> None:
        self._id = id
    
    @property
    def first_name(self) -> str:
        return self._first_name
    
    @first_name.setter
    def first_name(self, first_name: str | None) -> None:
        """
            - Length between 1 and 50 characters
            - Contains only letters, spaces, hyphens, or apostrophes
        """
        if first_name is None:
            raise ValueError('First name cannot be None')
        if not (1 <= len(first_name) <= 50):
            raise ValueError('First name must be between 1 and 50 characters long')
        if not re.match(r"^[a-zA-Z\s'-]+$", first_name):
            raise ValueError(f'{first_name} is not a valid name')
        self._first_name = first_name
        
    @property
    def last_name(self) -> str:
        return self._last_name
    
    @last_name.setter
    def last_name(self, last_name: str | None) -> None:
        if last_name is None:
            raise ValueError('Last name cannot be None')
        pattern =r'^(?P<name>[a-zA-Z]+)$'
        if re.search(pattern, last_name):
            self._last_name = last_name
        else:
            raise ValueError(f'{last_name} is not a valid name') 
        
    @property
    def username(self) -> str:
        return self._username
        
    @username.setter
    def username(self, username: str | None) -> None:
        """
        Validate a username.
        - Length between 3 and 20 characters
        - Contains only letters, numbers, underscores, or hyphens
        """
        if username is None:
            raise ValueError('Username cannot be None')
        if not (3 <= len(username) <= 20):
            raise ValueError('Username must be between 3 and 20 characters long')
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            raise ValueError(f'{username} is not a valid username')
        # Check if username already exists in the database
        db = get_db_connection()
        result = db.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
        if result:
            raise ValueError('Username already exists')
        self._username = username
        
    @property
    def date_of_birth(self) -> str:
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: str | None) -> None:
        """
        Validate a date of birth in the format YYYY/MM/DD.
        - Correct format
        - Real calendar date
        - Not in the future
        """
        # Check format with regex
        if date_of_birth is None:
            raise ValueError('Date of birth cannot be None')
        
        pattern = r"^(19|20)\d{2}/(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])$"
        if not re.match(pattern, date_of_birth):
            raise ValueError(f'{date_of_birth} is not a valid date of birth format')

        # Check if it's a real date and not in the future
        try:
            date_obj = datetime.strptime(date_of_birth, "%Y/%m/%d")
            today = datetime.today()
            if date_obj > today:
                raise ValueError('Date of birth cannot be in the future')
        except ValueError:
            # Handles impossible dates 
            raise ValueError(f'{date_of_birth} is not a real calendar date')
        self._date_of_birth = date_of_birth

        
    @property
    def password_hash(self) -> str:
        return self._password_hash
        
    @password_hash.setter
    def password_hash(self, password: str | None) -> None:
        """
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        """
        if password is None:
            raise ValueError('Password cannot be empty')
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[A-Z]", password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", password):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r"[0-9]", password):
            raise ValueError('Password must contain at least one number')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError('Password must contain at least one special character')
        self._password_hash = generate_password_hash(password)

    @property
    def created_at(self) -> datetime | str | None:
        return self._created_at
    
    @created_at.setter
    def created_at(self, created_at: datetime | str | None) -> None:
        self._created_at = created_at

        
        
    