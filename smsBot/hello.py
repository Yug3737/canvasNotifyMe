# Yug_API_KEY_pushbullet = "o.pRKGXgfyRf6v69A4Vwl0WkdQrkW8THQP"
import smtplib
from email.message import EmailMessage
from emailToSMSConfig import senderEmail, getawayAddress, appKey

msg = EmailMessage()
msg.set_content("Lets get a bag")

msg['From'] = senderEmail # 'email@address.com'
msg['To'] = getawayAddress #
msg['Subject'] = 'Hello from canvasNotifyMe!'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(senderEmail, appKey)

server.send_message(msg)
server.quit()