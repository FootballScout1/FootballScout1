import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from django.conf import settings
from config import Config

# smtp_server = 'smtp.gmail.com'
# smtp_port = 587
# sender_email = 'decencychukwuemekaukonu@gmail.com'
# receiver_email = 'ukonud4@gmail.com'
# password = 'ovzd iuwq jmel bbvz'
# EMAIL_USE_TLS = True

smtp_server = Config.MAIL_SERVER
smtp_port = Config.MAIL_PORT
sender_email = Config.MAIL_USERNAME
receiver_email = 'ukonud4@gmail.com'  
password = Config.MAIL_PASSWORD
EMAIL_USE_TLS = Config.MAIL_USE_TLS

message = MIMEMultipart("alternative")
message["Subject"] = "Test email"
message["From"] = sender_email
message["To"] = receiver_email

text = """\
Hello,
This is a test email."""

part1 = MIMEText(text, "plain")
message.attach(part1)

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {str(e)}")
