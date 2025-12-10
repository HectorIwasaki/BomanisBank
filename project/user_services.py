import sqlite3
from user import User

class UserServices:
    """Provides database and form utilities for user registration, login, and retrieval.
    Persistence layer for SQLite database"""
    
    @staticmethod
    def register_new_user(first_name: str, last_name: str, username: str, date_of_birth: str, password: str, db: sqlite3.Connection) -> User :
        """Creates a new user object from registration form data and inserts it into the database."""
        
        user = User(None, first_name, last_name, username, date_of_birth, password)
        cursor = db.execute(
            "INSERT INTO users (first_name, last_name, username, password_hash, date_of_birth) VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, username, user.password_hash, date_of_birth))
        db.commit()
        # The integer ID of the newly inserted row
        user_id = cursor.lastrowid 
        if user_id is None:
            raise ValueError("User could not be inserted into the database.")
        user.id = user_id
        return user
    
    @staticmethod
    def get_user_by_username(username: str, db: sqlite3.Connection) -> User | None:
        """Fetches a user by their username from the database."""
        row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not row:
            return None
        # construct User from DB row without re-validating password
        return User.from_row(row)
        

    @staticmethod
    def get_user_by_id(user_id: int, db: sqlite3.Connection) -> User | None:
        row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not row:
            return None  
        # Use the from_row factory to reconstruct a User without re-running constructor validation
        return User.from_row(row)

