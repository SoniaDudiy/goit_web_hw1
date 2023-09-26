from collections import UserDict
from datetime import datetime
import pickle
from abc import ABC, abstractmethod

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def is_valid_phone(self):
        pass 

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self.is_valid_phone(new_value):
            self.__value = new_value
        else:
            raise ValueError("Invalid phone number")        

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.")
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            self.__value == datetime.strptime(new_value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.")

class Record:
    def __init__(self, name: str, phones: list, emails: list, birthday: str = None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]
        self.emails = emails
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None        

    def delete_phone(self, value):
        phone_to_delete = self.find_phone(value)
        if phone_to_delete:
            self.phones.remove(phone_to_delete)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone

    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()
        return None             

class AddressBook(UserDict):
    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < len(self.data):
            key = list(self.data.keys())[self._iter_index]    
            value = self.data[key]
            self._iter_index += 1
            return (key, value)
        else:
            raise StopIteration
                
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)  

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass       

def search_handler(address_book, data):
    query = ' '.join(data).lower()
    matching_records = address_book.search(query)
    if matching_records:
        result = "Matching records:\n"
        for name, record in matching_records:
            phones = ', '.join([phone.value for phone in record.phones])
            result += f"{name}: {phones}\n"
    else:
        result = "No matching records found"
    return result

# Абстрактний базовий клас
class UserView(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def display(self):
        pass

class ContactView(UserView):
    def display(self):
        pass

class NoteView(UserView):
    def __init__(self, note_data):
        self.note_data = note_data
    def display(self):
        # Логіка для відображення нотаток на основі self.note_data
        pass
    
class CommandView(UserView):
    def __init__(self, available_commands):
        self.available_commands = available_commands

    def display(self):
        # Логіка для відображення доступних команд на основі self.available_commands
        pass

def main():
    address_book = AddressBook()
    address_book.load_from_file("address_book.pkl")

    contact_view = ContactView(address_book)
    note_data = [...] 
    note_view = NoteView(note_data)

    available_commands = ["add", "edit", "delete", "search", "exit"]
    command_view = CommandView(available_commands)

    while True:
        user_input = input(">>> ")
        if not user_input:
            continue
        func, data = command_parser(user_input)
        if not func:
            print("Unknown command. Type 'hello' for available commands.")
        else:
            result = func(contact_view, note_view, command_view, data)
            print(result)
            if func == exit_handler:
                address_book.save_to_file("address_book.pkl")
                break

if __name__ == "__main__":
    main()

