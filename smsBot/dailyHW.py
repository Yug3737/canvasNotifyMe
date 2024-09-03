#
# file: hello.py
# author: Yug Patel
# last modified: 24 Aug 2024
#

import smtplib
import os
import sys
import importlib.util
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

senderEmail = os.getenv('SENDER_EMAIL')
appKey = os.getenv('APP_KEY')

if not senderEmail or not appKey:
    print("Error: SENDER_EMAIL or APP_KEY env variables are not set.")
    sys.exit(1)

gatewayAddress = sys.argv[1]
notificationtime = sys.argv[2]
hw_str = sys.argv[3]

msg = EmailMessage()
msg.set_content(hw_str)

msg['From'] = senderEmail # 'email@address.com'
msg['To'] = gatewayAddress #
msg['Subject'] = 'Hello from canvasNotifyMe!'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(senderEmail, appKey)

server.send_message(msg)
server.quit()

print("SMS sent successfully")

if __name__ == "__main__":
    pass