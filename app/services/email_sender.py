import os
import smtplib
from email.message import EmailMessage
from app.models import Firsat
from app import db

def send_email(subject, to, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_ADDRESS')
    msg['To'] = to

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)
            print("Email sent successfully")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication error: {e}")
    except smtplib.SMTPConnectError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_opportunity_email_body():
    opportunities = Firsat.query.all()
    if not opportunities:
        return "No opportunities available at the moment."

    body = "Here are the current opportunities:\n\n"
    for opportunity in opportunities:
        body += (
            f"ID: {opportunity.id}\n"
            f"Product ID: {opportunity.urun_id}\n"
            f"Discount: {opportunity.indirim}\n"
            f"Start Date: {opportunity.baslangic_tarihi}\n"
            f"End Date: {opportunity.bitis_tarihi}\n\n"
        )
    return body

def send_opportunity_email(to):
    subject = "Current Opportunities"
    body = get_opportunity_email_body()
    send_email(subject, to, body)
