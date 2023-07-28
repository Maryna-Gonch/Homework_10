from collections import UserDict


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name: Name, *args: Phone):
        self.name = name
        self.phones = list(args)

    def add_phone(self, *args: Phone):
        self.phones.extend(args)

    def del_phone(self, *args: Phone):
        for phone in args:
            self.phones.remove(phone)

    def edit_phone(self, *args: Phone):
        self.phones = list(args)

    def __str__(self):
        return f"{self.name}: {', '.join(str(phone) for phone in self.phones)}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        self.data[record.name.value] = record
