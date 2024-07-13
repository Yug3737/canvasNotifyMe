import smtplib
from email.message import EmailMessage
from emailtoSMSConfig import senderEmail, appKey
import os
import sys
import importlib.util

# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, parent_dir)
# from app import gatewayAddress 

if len(sys.argv) != 2:
    print("Usage: python send_email.py <gatewayAddress>")
    sys.exit()

gatewayAddress = sys.argv[1]

msg = EmailMessage()
msg.set_content("\n Here would be your Canvas assignments that would be due within the next 14 days.")

msg['From'] = senderEmail # 'email@address.com'
msg['To'] = gatewayAddress #
msg['Subject'] = 'Hello from canvasNotifyMe!'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(senderEmail, appKey)

server.send_message(msg)
server.quit()

print("SMS sent successfully")