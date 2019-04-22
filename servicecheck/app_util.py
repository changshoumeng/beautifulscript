import time
import datetime

def gettickcount():
    current_time = time.time()
    return int(round(current_time * 1000))


def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')