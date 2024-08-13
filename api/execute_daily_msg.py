#
# Vercel function to be executed as an api endpoint 
# file: execute_hello.py
# author: Yug Patel
# last modified: 13 August 2024
# 
import os
import sys
import smtplib
from email.message import EmailMessage
import importlib.util
from dotenv import load_dotenv
load_dotenv()
import datetime

def handler(request):
    print("Entered handler")
    senderEmail = os.getenv('SENDER_EMAIL')
    appKey = os.getenv('APP_KEY')

    if not senderEmail or not appKey:
        print('Error obtaining SENDER_EMAIL or APP_KEY env variables are not set.')
        sys.exit()

    # make canvas get notification here and get the response text
    STUDENT_ACCESS_TOKEN = os.getenv('YUG_CANVAS_ACCESS_TOKEN')
    
    time_now = datetime.datetime.now()
    msg = EmailMessage()
    msg.set_content(f"The time is {time_now}. Which is adventure time.")

    gatewayAddress = "2166324947@vtext.com"
    msg['From'] = senderEmail
    msg['To'] = gatewayAddress
    msg['Subject'] = 'Hello from Canvas Notify Me!'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderEmail, appKey)

    server.send_message(msg)
    server.quit()
    print(f"Script {__file__} executed at {time_now}")
    print("Daily SMS sent successfully")

    # Perform scheduled task here
    return {
        "statusCode": 200,
        "body": "smsBot/hello.py executed successfully"
    }

if __name__ == "__main__":
    pass