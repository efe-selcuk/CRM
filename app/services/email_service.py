from flask_mail import Mail, Message
from app import create_app

app = create_app()
mail = Mail(app)

def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient], body=body)
    mail.send(msg)
