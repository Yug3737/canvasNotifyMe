# Yug_API_KEY_pushbullet = "o.pRKGXgfyRf6v69A4Vwl0WkdQrkW8THQP"
import smtplib
from email.message import EmailMessage
from emailtoSMSConfig import senderEmail, gatewayAddress, appKey

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