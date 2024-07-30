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

class Kategori(db.Model):
    id = Column(Integer, primary_key=True)
    ad = Column(String(50), unique=True, nullable=False)
    urunler = relationship('Urun', back_populates='kategori', lazy=True)

class Urun(db.Model):
    id = Column(String(8), primary_key=True)
    ad = Column(String(100), nullable=False)
    fiyat = Column(Float, nullable=False)
    stok_miktari = Column(Integer, nullable=False)
    kategori_id = Column(Integer, ForeignKey('kategori.id'), nullable=False)  # Her ürün bir kategoriye ait
    kategori = relationship('Kategori', back_populates='urunler')
    firsat = relationship('Firsat', backref='urun', uselist=False, lazy=True)

class Satis(db.Model):
    id = Column(String(8), primary_key=True)
    musteri_id = Column(String(8), ForeignKey('musteri.id'), nullable=False)
    tarih = Column(DateTime, nullable=False)
    toplam_tutar = Column(Float, nullable=False)
    musteri = relationship('Musteri', backref=db.backref('satislar', lazy=True))

class Firsat(db.Model):
    id = Column(String(8), primary_key=True)
    urun_id = Column(String(8), ForeignKey('urun.id'), unique=True, nullable=False)
    indirim = Column(Integer, nullable=False)
    baslangic_tarihi = Column(DateTime, nullable=False)
    bitis_tarihi = Column(DateTime, nullable=False)

class Aktivite(db.Model):
    id = Column(String(8), primary_key=True)
    musteri_id = Column(String(8), ForeignKey('musteri.id'), nullable=False)
    tarih = Column(DateTime, nullable=False)
    tur = Column(String(50), nullable=False)
    not_ = Column(String, nullable=False)
    musteri = relationship('Musteri', backref=db.backref('aktiviteler', lazy=True))

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
