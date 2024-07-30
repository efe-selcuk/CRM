from app import db

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
    not_ = db.Column(db.Text, nullable=True)
    musteri = db.relationship('Musteri', backref=db.backref('aktivite', lazy=True))
