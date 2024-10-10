import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
import logging
from config import (
    GMAIL_APP_PASSWORD,
    SENDER_EMAIL,
)

logger = logging.getLogger(__name__)

async def send_email(recipient_email, subject, body):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = recipient_email 
        message['Subject'] = subject
        
        message.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)  
        
        server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        server.quit()

        return True

    
    except Exception as e:
        logger.error(str(e))
        return False



async def random_password():
    return secrets.token_urlsafe(10)