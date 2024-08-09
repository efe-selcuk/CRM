import uuid
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Musteri(db.Model):
    id = Column(String(8), primary_key=True)
    isim = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    telefon = Column(String(20), nullable=False)
    adres = Column(String(200), nullable=False)
    alisveris_sikligi = Column(Float, nullable=False)
    sadakat_puani = Column(Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'isim': self.isim,
            'email': self.email,
            'telefon': self.telefon,
            'adres': self.adres,
            'alisveris_sikligi': self.alisveris_sikligi,
            'sadakat_puani': self.sadakat_puani
        }

class Kategori(db.Model):
    id = Column(Integer, primary_key=True)
    ad = Column(String(50), unique=True, nullable=False)
    urunler = relationship('Urun', back_populates='kategori', lazy=True)

class Urun(db.Model):
    id = Column(String(8), primary_key=True)
    ad = Column(String(100), nullable=False)
    fiyat = Column(Float, nullable=False)
    stok_miktari = Column(Integer, nullable=False)
    kategori_id = Column(Integer, ForeignKey('kategori.id'), nullable=False)
    kategori = relationship('Kategori', back_populates='urunler')
    firsat = relationship('Firsat', backref='urun', uselist=False, lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ad': self.ad,
            'fiyat': self.fiyat,
            'stok_miktari': self.stok_miktari,
            'kategori': self.kategori.ad if self.kategori else None
        }

class Satis(db.Model):
    id = Column(String(8), primary_key=True)
    musteri_id = Column(String(8), ForeignKey('musteri.id'), nullable=False)
    tarih = Column(DateTime, nullable=False)
    toplam_tutar = Column(Float, nullable=False)
    musteri = relationship('Musteri', backref=db.backref('satislar', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'musteri_id': self.musteri_id,
            'tarih': self.tarih.strftime('%Y-%m-%d %H:%M:%S'),
            'toplam_tutar': self.toplam_tutar
        }

class Firsat(db.Model):
    id = Column(String(8), primary_key=True)
    urun_id = Column(String(8), ForeignKey('urun.id'), unique=True, nullable=False)
    indirim = Column(Integer, nullable=False)
    baslangic_tarihi = Column(DateTime, nullable=False)
    bitis_tarihi = Column(DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'urun_id': self.urun_id,
            'indirim': self.indirim,
            'baslangic_tarihi': self.baslangic_tarihi.strftime('%Y-%m-%d'),
            'bitis_tarihi': self.bitis_tarihi.strftime('%Y-%m-%d')
        }

class Aktivite(db.Model):
    id = Column(String(8), primary_key=True)
    musteri_id = Column(String(8), ForeignKey('musteri.id'), nullable=False)
    tarih = Column(DateTime, nullable=False)
    tur = Column(String(50), nullable=False)
    not_ = Column(String, nullable=False)
    musteri = relationship('Musteri', backref=db.backref('aktiviteler', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'musteri_id': self.musteri_id,
            'tarih': self.tarih.strftime('%Y-%m-%d %H:%M:%S'),
            'tur': self.tur,
            'not': self.not_
        }

class Personel(db.Model):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isim = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    sifre_hash = Column(String(128), nullable=False)
    rol = Column(String(50), nullable=False)
    
    def set_password(self, sifre):
        self.sifre_hash = generate_password_hash(sifre)
    
    def check_password(self, sifre):
        return check_password_hash(self.sifre_hash, sifre)
    
    def to_dict(self):
        return {
            'id': self.id,
            'isim': self.isim,
            'email': self.email,
            'rol': self.rol
        }
