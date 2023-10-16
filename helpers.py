from string import ascii_letters, digits
import re

def is_password_ok(password):
    regex = "[^0-9a-zA-Z]+"
    if re.search(regex, password):
        print("OK")
    return False

def is_username_ok(username):
    regex = "[^0-9a-zA-Z]+"
    if re.search(regex, username):
        print("OK")

    return False