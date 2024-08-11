import smtplib
from email.message import EmailMessage
import os
import sys
import importlib.util
from dotenv import load_dotenv
load_dotenv()

if len(sys.argv) != 2:
    print("usage: python hello.py <gatewayAddress>")
    sys.exit()

senderEmail = os.getenv('SENDER_EMAIL')
appKey = os.getenv('APP_KEY')

if not senderEmail or not appKey:
    print("Error: SENDER_EMAIL or APP_KEY env variables are not set.")
    sys.exit(1)

gatewayAddress = sys.argv[1]
notificationtime = sys.argv[2]

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

if __name__ == "__main__":
    main()