"""
TASK 1
Write console program for storing data about contacts. Each contact should contain name and phone number.
Program should provide an ability to create new contact, find phone number by name,
change phone number by name and remove contact by name.

TASK 2
Separate IO from business-logic
Write decorator to check if contact exists
Provide functions for storing and loading data in pickle format
"""

import pickle
import functools
import re
from os import path

CONTACTS_PATH = path.join(path.dirname(path.abspath(__file__)), "contacts.pickle")


def read_from_pickle(contacts_path):
    with open(contacts_path, "rb") as file_reader:
        try:
            yield pickle.load(file_reader)
        except EOFError:
            pass


def load_contacts():
    contacts = {}
    generator_object = read_from_pickle(CONTACTS_PATH)
    while True:
        try:
            contacts.update(next(generator_object))
        except (StopIteration, FileNotFoundError):
            break
    return contacts


def get_valid_data(pattern, data_type):
    for _ in range(0, 3):
        input_value = input(f"Insert {data_type}: ").strip()
        matched_pattern = re.match(pattern, input_value).group(0)
        # the full inserted string should match the pattern
        if matched_pattern != input_value:
            print(f"Invalid {data_type}, try again")
        else:
            return matched_pattern

    print("""Failed to insert valid name.
Exiting to main menu""")
    main()


def check_contact(invert_condition, log_msg):
    def check_contact_decorator(func):
        functools.wraps(func)

        def wrapper(contacts):
            valid_name = get_valid_name()
            condition = (valid_name not in contacts) if invert_condition else (valid_name in contacts)
            if condition:
                return func(contacts, valid_name)
            else:
                print(log_msg)

        return wrapper

    return check_contact_decorator


def get_valid_name():
    return get_valid_data(r"[a-zA-Z\s]*", "name")


def get_valid_phone_number():
    return get_valid_data(r"[0-9]*", "phone number")


@check_contact(invert_condition=True, log_msg="Contact already exists")
def add_contact(contacts, name):
    contacts[name] = get_valid_phone_number()
    print(f"User {name} added to contacts.")


@check_contact(invert_condition=False, log_msg="Contact doesn't exist")
def edit_contact(contacts, name):
    contacts[name] = get_valid_phone_number()
    print(f"User {name} was updated.")


@check_contact(invert_condition=False, log_msg="Contact doesn't exist")
def delete_contact(contacts, name):
    del contacts[name]
    print(f"User {name} was deleted.")


@check_contact(invert_condition=False, log_msg="Contact doesn't exist")
def find_contact(contacts, name):
    print(f"{name}: {contacts[name]}")


def store_contacts(contacts):
    with open(CONTACTS_PATH, "wb") as file_writer:
        pickle.dump(contacts, file_writer)


def close(contacts):
    store_contacts(contacts)
    print("Database Saved.")
    exit()


def print_menu():
    for key, value in OPTION_DICT.items():
        print(f"{key}: {value['description']}")


def get_user_input():
    while True:
        user_input = input("Please insert option from the menu: ").strip().upper()
        if user_input in OPTION_DICT:
            OPTION_DICT[user_input]["function"](*OPTION_DICT[user_input]["args"])
        else:
            print("Invalid option, please try again.")


def main():
    print_menu()
    get_user_input()


if __name__ == '__main__':
    CONTACTS = load_contacts()
    OPTION_DICT = {
        "A": {
            "description": "Add new contact",
            "function": add_contact,
            "args": [CONTACTS],
        },
        "F": {
            "description": "Find existing contact",
            "function": find_contact,
            "args": [CONTACTS],
        },
        "E": {
            "description": "Edit existing contact",
            "function": edit_contact,
            "args": [CONTACTS],
        },
        "D": {
            "description": "Delete existing contact",
            "function": delete_contact,
            "args": [CONTACTS],
        },
        "Q": {
            "description": "Quit",
            "function": close,
            "args": [CONTACTS],
        }
    }

    main()
