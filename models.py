from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Kullanıcı(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    isim = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    şifre = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
