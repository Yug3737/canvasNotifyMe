#
# Vercel function to be executed as an api endpoint 
# file: execute_hello.py
# author: Yug Patel
# last modified: 12 August 2024
# 
import os
import datetime

def handler(request):
    # Python script code here
    now = datetime.datetime.now()
    print(f"Script executed {now}")

    # Perform scheduled task here
    return {
        "statusCode": 200,
        "body": "smsBot/hello.py executed successfully"
    }