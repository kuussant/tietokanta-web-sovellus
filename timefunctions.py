from datetime import datetime
def convert_time(time):

    current_time = datetime.now()
    #time = "2023-10-14 1:06:13.852441"
    #current_time = string_to_datetime("2023-10-19 1:06:27.852441")
    
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
    

def string_to_datetime(time):

    time_split = time.split(".")[0].split(" ")
    ymd = time_split[0].split("-")
    hms = time_split[1].split(":")

    ymdhms = []
    for t in ymd:
        ymdhms.append(int(t))

    for t in hms:
        ymdhms.append(int(t))

    return datetime(ymdhms[0], ymdhms[1], ymdhms[2], ymdhms[3], ymdhms[4], ymdhms[5])