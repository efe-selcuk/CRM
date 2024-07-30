import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import Config
from models import db, Aktivite, Müşteri, Ürün
from datetime import datetime
from app import app

def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = Config.EMAIL_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
            server.sendmail(Config.EMAIL_ADDRESS, to_address, msg.as_string())
        print("E-posta başarıyla gönderildi!")
    except Exception as e:
        print(f"E-posta gönderilemedi: {e}")

def send_reminders():
    with app.app_context():
        today = datetime.now().date()
        activities = Aktivite.query.filter(db.func.date(Aktivite.tarih) == today).all()

        for activity in activities:
            customer = Müşteri.query.get(activity.müşteri_id)
            product = Ürün.query.order_by(db.func.random()).first()  # Rastgele bir ürün seç

            subject = f"{activity.tür} Hatırlatma"
            body = (f"Merhaba {customer.isim},\n\n"
                    f"Bugün için bir {activity.tür} hatırlatmanız var.\n\n"
                    f"Ürün: {product.ad}\n"
                    f"Kategori: {product.kategori}\n\n"
                    f"Not: {activity.not_}\n\n"
                    f"İyi günler!")

            send_email(customer.email, subject, body)

if __name__ == "__main__":
    send_reminders()
