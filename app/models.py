from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Musteri(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    isim = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    adres = db.Column(db.String(200), nullable=False)
    alisveris_sikligi = db.Column(db.Float, nullable=False)
    sadakat_puani = db.Column(db.Float, nullable=False)

class Urun(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    fiyat = db.Column(db.Float, nullable=False)
    stok_miktari = db.Column(db.Integer, nullable=False)

class Satis(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    musteri_id = db.Column(db.String(8), db.ForeignKey('musteri.id'), nullable=False)
    tarih = db.Column(db.DateTime, nullable=False)
    toplam_tutar = db.Column(db.Float, nullable=False)
    musteri = db.relationship('Musteri', backref=db.backref('satislar', lazy=True))

class Firsat(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    urun_id = db.Column(db.String(8), db.ForeignKey('urun.id'), nullable=False)
    indirim = db.Column(db.Integer, nullable=False)
    baslangic_tarihi = db.Column(db.DateTime, nullable=False)
    bitis_tarihi = db.Column(db.DateTime, nullable=False)
    urun = db.relationship('Urun', backref=db.backref('firsatlar', lazy=True))

class Aktivite(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    musteri_id = db.Column(db.String(8), db.ForeignKey('musteri.id'), nullable=False)
    tarih = db.Column(db.DateTime, nullable=False)
    tur = db.Column(db.String(50), nullable=False)
    not_ = db.Column(db.Text, nullable=False)
    musteri = db.relationship('Musteri', backref=db.backref('aktiviteler', lazy=True))

class Personel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sifre_hash = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.sifre_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.sifre_hash, password)
