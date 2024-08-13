#
# Script to trigger trigger_execute_daily_msg.py
# file: trigger_execute_hello.py
# author: Yug Patel
# last modified: 12 August 2024
# 
import os
import time
import schedule
import requests
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

""" This script is supposed to be running continouosly and triggering vercel function which is located in api/execute_hello.py
    """
def trigger_execute_daily_msg():
    url = "https://canvas-notify-me.vercel.app/api/execute_hello"
    response = requests.get(url)
    print(f"Triggered vercel function execute_hello.py. Status Code:  {response.status_code}")

SUPABASE_PROJECT_URL = os.getenv('SUPABASE_PROJECT_URL')
SUPABASE_SECRET_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SECRET_SERVICE_ROLE_KEY')

supabase_client = create_client(SUPABASE_PROJECT_URL, SUPABASE_SECRET_SERVICE_ROLE_KEY)

def get_notification_time(id: str) -> str:
    try:
        response = supabase_client\
                .table('Student')\
                .select('notification_time')\
                .eq('id', id)\
                .single()\
                .execute()

        data = response.data
        if data:
            if len(data) == 1:
                return data['notification_time']
            else:
                return f"Multiple records found. Expexted only one."
        else:
            return "No record found."
    except Exception as err:
        return f"Error occured wile executing get_notification_time: {err}"
# Hardcoding id for myself right now
id = 36
notificationTime = get_notification_time(id)
notificationTime = "09:21"
# Schedule acccording to time
print("notificationTime is", notificationTime)
schedule.every().day.at(notificationTime).do(trigger_execute_daily_msg)

while True:
    schedule.run_pending()
    time.sleep(60)