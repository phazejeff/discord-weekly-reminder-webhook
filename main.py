import schedule
import random
import requests
import time


WEBHOOK_URL = 'PUT WEBHOOK URL HERE'
REMIND_BEFORE = 5 # minutes before

def get_data(file):
    f = open(file)
    data = eval(f.read())
    f.close()
    return data

def subtract_minute(hour, minute, sub):
    minute -= sub
    if minute < 0:
        minute += 60
        hour -= 1
        if hour < 0:
            hour += 24
    return hour, minute

def send(isNoon, hour, minute):
    data = get_data('messages.txt')
    if hour > 12:
        hour -= 12
    if isNoon:
        message = {
            'content' : data['noon'][random.randint(0, len(data['noon'])-1)].replace('%h', str(hour)).replace('%m', str(minute))
        }
        requests.post(WEBHOOK_URL, data=message)
    else:
        message = {
            'content' : data['session'][random.randint(0, len(data['session'])-1)].replace('%h', str(hour)).replace('%m', str(minute))
        }
        requests.post(WEBHOOK_URL, data=message)


def convert_hour_minute_to_string(hour, minute):
    if len(str(hour)) == 1:
        time = f"0{str(hour)}:"
    else:
        time = f"{str(hour)}:"
    if len(str(minute)) == 1:
        time += f"0{str(minute)}"
    else:
        time += str(minute)
    
    return time

def set_schedule(arr):
    # arr: array [day, hour, minute] with 0 as monday and 6 as sunday
    hour, minute = arr[1], arr[2]
    remind_hour, remind_minute = subtract_minute(arr[1], arr[2], REMIND_BEFORE)
    
    time = convert_hour_minute_to_string(remind_hour, remind_minute)

    early_remind_hour, early_remind_minute = 14, 0
    early_remind = convert_hour_minute_to_string(early_remind_hour, early_remind_minute)

    if arr[0] == 0:
        schedule.every().monday.at(early_remind).do(send, True, hour, minute)
        schedule.every().monday.at(time).do(send, False, hour, minute)
    elif arr[0] == 1:
        schedule.every().tuesday.at(early_remind).do(send, True, hour, minute)
        schedule.every().tuesday.at(time).do(send, False, hour, minute)
    elif arr[0] == 2:
        schedule.every().wednesday.at(early_remind).do(send, True, hour, minute)
        schedule.every().wednesday.at(time).do(send, False, hour, minute)
    elif arr[0] == 3:
        schedule.every().thursday.at(early_remind).do(send, True, hour, minute)
        schedule.every().thursday.at(time).do(send, False, hour, minute)
    elif arr[0] == 4:
        schedule.every().friday.at(early_remind).do(send, True, hour, minute)
        schedule.every().friday.at(time).do(send, False, hour, minute)
    elif arr[0] == 5:
        schedule.every().saturday.at(early_remind).do(send, True, hour, minute)
        schedule.every().saturday.at(time).do(send, False, hour, minute)
    elif arr[0] == 6:
        schedule.every().sunday.at(early_remind).do(send, True, hour, minute)
        schedule.every().sunday.at(time).do(send, False, hour, minute)

def main():
    times = get_data('times.txt')
    for i in times:
        set_schedule(i)

if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)