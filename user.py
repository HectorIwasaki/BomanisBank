from datetime import date
from account_library import AccountLibrary
import re

class User:
     
    def __init__(self, first_name, last_name, birthday, pin,) -> None:      
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.pin = pin
        self.user_id = self.first_name + self.last_name
        self.checkings_library = AccountLibrary()
        self.savings_library = AccountLibrary()
    
    def __str__(self) -> str:
        return f'''Name: {self.first_name} {self.last_name}\
        Birthday: {self.birthday}\
        User ID: {self.user_id}\
        Pin: {self.pin}'''
            
    @property
    def first_name(self) -> str:
        return self._first_name
    
    @first_name.setter
    def first_name(self, first_name) -> None:
        pattern =r'^(?P<name>[a-zA-Z]+)$'
        if re.search(pattern, first_name):
            self._first_name = first_name
        else:
            raise ValueError(f'{first_name} is not a valid name')
        
    @property
    def last_name(self) -> str:
        return self._last_name
    
    @last_name.setter
    def last_name(self, last_name) -> None:
        pattern =r'^(?P<name>[a-zA-Z]+)$'
        if re.search(pattern, last_name):
            self._last_name = last_name
        else:
            raise ValueError(f'{last_name} is not a valid name')
    
    @property
    def birthday(self) -> date:
        return self._birthday
    
    @birthday.setter
    def birthday(self, birthday) -> None:
        if birthday:= date.fromisoformat(birthday):
            self._birthday = birthday
        else:
            raise ValueError('Birthday must be in the format YYYY-MM-DD')
        
    @property
    def pin(self) -> str:
        return self._pin
    
    @pin.setter
    def pin(self, pin) -> None:
        pattern = r'^(?P<pin>[1-9]{4})$'
        if re.search(pattern,pin):
            self._pin = pin
        else:
            raise ValueError('{pin} is not a valid pin')
        
    