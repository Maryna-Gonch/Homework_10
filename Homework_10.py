import address_book


def sanitize_number(number: str) -> str:
    number = number.replace(
        "-", "").replace("(", "").replace(")", "").replace("_",  "")
    if any(not char.isnumeric() for char in number.removeprefix('+')):
        return ""
    if len(number) == 10:
        return '+38' + number
    if len(number) == 12:
        return '+' + number
    if len(number) == 13:
        return number
    return ""


phones = address_book.AddressBook()


def invalid_command(inp) -> str:
    return f"Invalid command: {inp}"


def input_error(func):
    def wrap(input_data):
        try:
            return func(*input_data)
        except (IndexError, ValueError, TypeError):
            return f"Not valid number of arguments ({len(input_data)} were given). Required: {func.__doc__}"
        except KeyError:
            return f"Incorrect name to get phone, contact doesn't exist"
    return wrap


@input_error
def greet() -> str:
    """
    No arguments reqires for this function"""
    return "How can I help you?"


@input_error
def add_contact(name: str, *args: str) -> str:
    """
    Name - contact name without space (Ihor, Magnus_Carlsen, e.t.c)
    Phone - contact phone number without spaces (+380123467895, +38(096)1267908, e.t.c)"""
    if name in phones:
        return "Contact exists! You can only change this contact"

    lst_phones: list[address_book.Phone] = []
    for phone_ in args:
        new_phone = sanitize_number(phone_)
        if not new_phone:
            return f"Invalid mobile phone: {phone_}. Required length 10, 12 (only digits) or 13 ('+' on begining)"
        lst_phones.append(address_book.Phone(new_phone))

    record = address_book.Record(address_book.Name(name), *lst_phones)
    phones.add_record(record)
    return f"Succesfully added new contact. {record}"


@input_error
def change(name: str, *args: str) -> str:
    """
    Name - contact to change name without space (Ihor, Magnus_Carlsen, e.t.c)
    Phone - new contact phone number without spaces (+380123467895, +38(096)1267908, e.t.c)"""

    if not (name in phones):
        return "Contact exists! You can only change this contact"

    lst_phones: list[address_book.Phone] = []
    for phone_ in args:
        new_phone = sanitize_number(phone_)
        if not new_phone:
            return f"Invalid mobile phone: {phone_}. Required length 10, 12 (only digits) or 13 ('+' on begining)"
        lst_phones.append(address_book.Phone(new_phone))

    record = address_book.Record(address_book.Name(name), *lst_phones)
    phones.add_record(record)
    return f"Succesfully changed contact. {record}"


@input_error
def phone(name: str) -> str:
    """
    Name - contact to print phone without space (Ihor, Magnus_Carlsen, e.t.c)"""

    return f"Contact {phones[name]}"


@input_error
def show_all() -> str:
    """
    No arguments reqires for this function"""
    if not len(phones):
        return "You don't have contacts!"
    answ = "Here is your list of contacts:\n"
    for i, record in enumerate(phones.values()):
        answ += f"    {i+1}. {record}\n"
    return answ[:-1]


@input_error
def bye(*args: str) -> str:
    """
    No arguments reqires for this function"""
    return "Good bye!"


RESPONSES = {
    "hello": greet,
    "add": add_contact,
    "change": change,
    "phone": phone,
    "show all": show_all,
    "good bye": bye,
    "close": bye,
    "exit": bye
}


def parse_input(user_input: str) -> tuple:
    user_input = user_input.strip()
    lower_input = user_input.lower()
    for key in RESPONSES:
        if lower_input.startswith(key):
            func, args = RESPONSES[key], user_input[len(
                key)+1:].strip().split()
            return func, args
    return invalid_command, user_input


def main():
    print("Welcome!\n")
    answer = ""
    while answer != "Good bye!":
        user_input = input("Please, enter command: ")
        func, args = parse_input(user_input)
        answer = func(args)
        print(answer)
        print()


if __name__ == '__main__':
    main()
