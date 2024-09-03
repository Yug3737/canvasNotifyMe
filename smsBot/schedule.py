#
# file: schedule.py
# author: Yug Patel
# last modified: 2 Sep 2024
#

import os
import time
import subprocess
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client
from functions import get_gateway_address
from canvas_api import get_hws_due, get_hw_dict_from_course_ids, get_current_time_string_iso, get_user_profile

SUPABASE_PROJECT_URL = os.environ.get("SUPABASE_PROJECT_URL")
SUPABASE_SECRET_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SECRET_SERVICE_ROLE_KEY")

if not SUPABASE_PROJECT_URL:
    raise ValueError("SUPABASE_PROJECT_URL is not set")
elif not SUPABASE_SECRET_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_SECRET_SERVICE_ROLE_KEY is not set")

supabase = create_client(SUPABASE_PROJECT_URL, SUPABASE_SECRET_SERVICE_ROLE_KEY)

# This file is supposed to continuously run and check if current time is equal to any of the times chosen by the users in the database
# Dictionary {"HH:MM":count}, count is the number of people in the database who chose "HH:MM" as their daily notification time

notification_times = {
    "20:11": 2,
    "20:12": 2,
    "20:13": 2,
    "20:14": 2,
    "20:15": 2,
    "20:16": 2,
    "20:17": 2,
    "20:18": 2,
    "20:09": 2,
    "20:10": 2,
}

def check_notification_times():
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([env.get('PYTHONPATH', ''), os.path.abspath(os.path.dirname(__file__))])

    while True:
        curr_time = datetime.now().strftime('%H:%M')
        if curr_time in notification_times:

            response = supabase.table("Student").select("*").eq("notification_time", curr_time).execute()
            print("response =>", response)
            assert len(response.data) > 0 

            for student in response.data:
                notification_time = student["notification_time"]
                gatewayAddress = get_gateway_address(student["cell_number"], student["cell_carrier"])
                try:
                    user_profile = get_user_profile()
                    user_id = user_profile.get('id')
                    hw_dict = get_hws_due(get_hw_dict_from_course_ids(
                        user_id), get_current_time_string_iso())
                    hw_str = str()
                    for key,value in hw_dict.items():
                        hw_str += key + ": " + value + "\n"
                    result = subprocess.run(['python', 'smsBot/dailyHW.py', gatewayAddress, notification_time, hw_str],
                                            capture_output=True,
                                            text=True, 
                                            env=env)
                    print(result.stdout)
                    if result.returncode != 0:
                        print("schedule.py encountered an error")
                        print(result.stderr)
                except Exception as e:
                    print(f"Error running subprocess: {e}")
                time.sleep(15)


    
if __name__ == "__main__":
    print("Schedule.py is checking for notification Times")
    check_notification_times()