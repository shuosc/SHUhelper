import time
def this_week():
    #start_week = -
    #return int(time.strftime("%W"))-start_week
    return 6

def this_day():
    return int(time.strftime("%w"))

def this_class():
    ctime = int(time.strftime("%H%M"))
    if ctime <= 800:
        return 0
    elif ctime <= 845:
        return 1
    elif ctime <= 940:
        return 2
    elif ctime <= 1045:
        return 3
    elif ctime <= 1140:
        return 4
    elif ctime <= 1255:
        return 5
    elif ctime <= 1350:
        return 6
    elif ctime <= 1455:
        return 7
    elif ctime <= 1550:
        return 8
    elif ctime <= 1645:
        return 9
    elif ctime <= 1740:
        return 10
    elif ctime <= 1845:
        return 11
    elif ctime <= 1940:
        return 12
    elif ctime <= 2035:
        return 13
    else:
        return 0
