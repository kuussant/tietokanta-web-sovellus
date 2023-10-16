import re


def is_pass_secure(password):
    lower_ok = False
    upper_ok = False
    digit_ok = False
    special_ok = False

    if re.search("[a-z]+", password):
        lower_ok = True
    if re.search("[A-Z]+", password):
        upper_ok = True
    if re.search("[0-9]+", password):
        digit_ok = True
    if re.search("[^0-9a-zA-Z]+", password):
        special_ok = True

    if lower_ok and upper_ok and digit_ok and special_ok:
        return True
    return False


def contains_specials(str):
    regex = "[^0-9a-zA-Z]+"
    if re.search(regex, str):
        return True
    return False