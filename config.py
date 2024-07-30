# config.py
import datetime

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crm.db'
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Güvenli bir anahtar belirleyin
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)  # Token süresi

    # E-posta ayarları
    EMAIL_ADDRESS = 'efeselcuk007@gmail.com'
    EMAIL_PASSWORD = 'zifl kxce ulmi whva'
