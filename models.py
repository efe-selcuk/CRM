from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Kullanıcı(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    isim = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    şifre = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

class Müşteri(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    isim = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefon = db.Column(db.String(20))
    adres = db.Column(db.String(255))
    alışveriş_sıklığı = db.Column(db.Float)
    sadakat_puanı = db.Column(db.Float)

class Ürün(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    ad = db.Column(db.String(100))
    kategori = db.Column(db.String(50))
    fiyat = db.Column(db.Float)
    stok_miktarı = db.Column(db.Integer)

class Satış(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    müşteri_id = db.Column(db.String(36), db.ForeignKey('müşteri.id'))
    tarih = db.Column(db.DateTime)
    toplam_tutar = db.Column(db.Float)
    müşteri = db.relationship('Müşteri', backref=db.backref('satışlar', lazy=True))

class Fırsat(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    ürün_id = db.Column(db.String(36), db.ForeignKey('ürün.id'))
    indirim = db.Column(db.Float)
    başlangıç_tarihi = db.Column(db.DateTime)
    bitiş_tarihi = db.Column(db.DateTime)
    ürün = db.relationship('Ürün', backref=db.backref('fırsatlar', lazy=True))

class Aktivite(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    müşteri_id = db.Column(db.String(36), db.ForeignKey('müşteri.id'))
    tarih = db.Column(db.DateTime)
    tür = db.Column(db.String(50))
    not_ = db.Column(db.String(255))
    müşteri = db.relationship('Müşteri', backref=db.backref('aktiviteler', lazy=True))
