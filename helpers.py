import re

from datetime import datetime

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


def convert_time(time):

    current_time = datetime.now()

    delta = current_time-time

    seconds = delta.total_seconds()

    s_y = 31536000
    s_mon = 2629743
    s_d = 86400
    s_h = 3600
    s_min = 60

    time_string = None
    t = 0

    #years
    if seconds >= s_y:
        t = seconds // s_y
        time_string = f"year" if t == 1 else f"years"

    #months
    elif seconds >= s_mon:
        t = seconds // s_mon
        time_string = f"month" if t == 1 else f"months"
    
    #days
    elif seconds >= s_d:
        t = seconds // s_d
        time_string = f"day" if t == 1 else f"days"

    #hours
    elif seconds >= s_h:
        t = seconds // s_h
        time_string = f"hour" if t == 1 else f"hours"

    #minutes
    elif seconds >= s_min:
        t = seconds // s_min
        time_string = f"minute" if t == 1 else f"minutes"
    
    #seconds
    else:
        return "Now"

    return f"{int(t)} {time_string} ago"

def __by_date(item):
    return item.created_at

def sort_by_date_newest(items):
    return sorted(items, key=__by_date, reverse=True)

def sort_by_date_oldest(items):
    return sorted(items, key=__by_date, reverse=False)