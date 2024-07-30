# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config  # Config sınıfını import edin

def send_email(to_email, subject, body):
    from_email = Config.EMAIL_ADDRESS
    password = Config.EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"E-posta gönderildi: {to_email}\nKonu: {subject}\nİçerik: {body}")
    except Exception as e:
        print(f"E-posta gönderilemedi: {str(e)}")
