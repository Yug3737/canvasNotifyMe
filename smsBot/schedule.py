#
# file: schedule.py
# author: Yug Patel
# last modified: 31 Aug 2024
#

import os
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# This file is supposed to continuously run and check if current time is equal to any of the times chosen by the users in the database
# Dictionary {"HH:MM":count}, count is the number of people in the database who chose "HH:MM" as their daily notification time

notification_times = {
}

def check_notification_times():
    while True:
        curr_time = datetime.now().strftime('%H:%M')
        if curr_time in notification_times:
            count = notification_times[curr_time]
    
if __name__ == "__main__":
    print("Schedule.py is checking for notification Times")
    check_notification_times()