from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from cryptography.fernet import Fernet
import uuid
import datetime

# Flask uygulaması ve konfigürasyon
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Güvenli bir anahtar kullanmalısınız
app.config['RATE_LIMIT'] = '200 per day;50 per hour'

db = SQLAlchemy(app)
jwt = JWTManager(app)
limiter = Limiter(get_remote_address, app=app)

# Şifreleme için Fernet anahtarı
fernet_key = Fernet.generate_key()
fernet = Fernet(fernet_key)

# Veritabanı modelleri
class Müşteri(db.Model):
    id = db.Column(db.String, primary_key=True)
    isim = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    telefon = db.Column(db.String, nullable=False)
    adres = db.Column(db.String, nullable=False)
    şirket = db.Column(db.String, nullable=False)
    oluşturulma_tarihi = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    güncellenme_tarihi = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Fırsat(db.Model):
    id = db.Column(db.String, primary_key=True)
    müşteri_id = db.Column(db.String, db.ForeignKey('müşteri.id'), nullable=False)
    başlangıç_tarihi = db.Column(db.DateTime, nullable=False)
    bitiş_tarihi = db.Column(db.DateTime, nullable=False)
    aşama = db.Column(db.String, nullable=False)
    toplam_tutar = db.Column(db.Float, nullable=False)
    açıklama = db.Column(db.String, nullable=False)
    oluşturulma_tarihi = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    güncellenme_tarihi = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Aktivite(db.Model):
    id = db.Column(db.String, primary_key=True)
    müşteri_id = db.Column(db.String, db.ForeignKey('müşteri.id'), nullable=False)
    tarih = db.Column(db.DateTime, nullable=False)
    tür = db.Column(db.String, nullable=False)
    not_ = db.Column('not', db.String, nullable=False)  # 'not' yerine 'not_' kullanıyoruz
    sonuç = db.Column(db.String, nullable=False)
    oluşturulma_tarihi = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    güncellenme_tarihi = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Kullanıcı(db.Model):
    id = db.Column(db.String, primary_key=True)
    isim = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    rol = db.Column(db.String, nullable=False)
    oluşturulma_tarihi = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    güncellenme_tarihi = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# API Uç Noktaları

@app.route('/kayit', methods=['POST'])
def kayit():
    data = request.get_json()
    yeni_kullanıcı = Kullanıcı(
        id=str(uuid.uuid4()),
        isim=data['isim'],
        email=data['email'],
        rol=data['rol']
    )
    db.session.add(yeni_kullanıcı)
    db.session.commit()
    return jsonify({"mesaj": "Kullanıcı başarıyla kaydedildi!"}), 201

@app.route('/giris', methods=['POST'])
def giris():
    data = request.get_json()
    kullanıcı = Kullanıcı.query.filter_by(email=data['email']).first()
    if kullanıcı:
        access_token = create_access_token(identity={"id": kullanıcı.id, "rol": kullanıcı.rol})
        return jsonify(access_token=access_token), 200
    return jsonify({"mesaj": "Geçersiz kimlik bilgileri"}), 401

@app.route('/müşteriler', methods=['POST'])
@jwt_required()
def müşteri_ekle():
    mevcut_kullanıcı = get_jwt_identity()
    if mevcut_kullanıcı['rol'] not in ['Admin']:
        return jsonify({"mesaj": "İzin reddedildi"}), 403

    data = request.get_json()
    şifrelenmiş_email = fernet.encrypt(data['email'].encode()).decode()
    müşteri = Müşteri(
        id=str(uuid.uuid4()),
        isim=data['isim'],
        email=şifrelenmiş_email,
        telefon=data['telefon'],
        adres=data['adres'],
        şirket=data['şirket']
    )
    db.session.add(müşteri)
    db.session.commit()
    return jsonify({"mesaj": "Müşteri başarıyla eklendi!"}), 201

@app.route('/fırsatlar', methods=['POST'])
@jwt_required()
def fırsat_ekle():
    mevcut_kullanıcı = get_jwt_identity()
    if mevcut_kullanıcı['rol'] not in ['Admin', 'Satış Temsilcisi']:
        return jsonify({"mesaj": "İzin reddedildi"}), 403

    data = request.get_json()
    fırsat = Fırsat(
        id=str(uuid.uuid4()),
        müşteri_id=data['müşteri_id'],
        başlangıç_tarihi=datetime.datetime.fromisoformat(data['başlangıç_tarihi']),
        bitiş_tarihi=datetime.datetime.fromisoformat(data['bitiş_tarihi']),
        aşama=data['aşama'],
        toplam_tutar=data['toplam_tutar'],
        açıklama=data['açıklama']
    )
    db.session.add(fırsat)
    db.session.commit()
    return jsonify({"mesaj": "Fırsat başarıyla eklendi!"}), 201

@app.route('/aktivite', methods=['POST'])
@jwt_required()
def aktivite_ekle():
    mevcut_kullanıcı = get_jwt_identity()
    if mevcut_kullanıcı['rol'] not in ['Admin', 'Satış Temsilcisi', 'Müşteri Hizmetleri']:
        return jsonify({"mesaj": "İzin reddedildi"}), 403

    data = request.get_json()
    aktivite = Aktivite(
        id=str(uuid.uuid4()),
        müşteri_id=data['müşteri_id'],
        tarih=datetime.datetime.fromisoformat(data['tarih']),
        tür=data['tür'],
        not_=data['not'],  # 'not' yerine 'not_' kullanıyoruz
        sonuç=data['sonuç']
    )
    db.session.add(aktivite)
    db.session.commit()
    return jsonify({"mesaj": "Aktivite başarıyla eklendi!"}), 201

@app.route('/kullanıcılar', methods=['GET'])
@jwt_required()
@limiter.limit("5 per minute")
def kullanıcılar_getir():
    mevcut_kullanıcı = get_jwt_identity()
    if mevcut_kullanıcı['rol'] not in ['Admin']:
        return jsonify({"mesaj": "İzin reddedildi"}), 403

    kullanıcılar = Kullanıcı.query.all()
    kullanıcılar_listesi = [{"id": kullanıcı.id, "isim": kullanıcı.isim, "email": kullanıcı.email, "rol": kullanıcı.rol} for kullanıcı in kullanıcılar]
    return jsonify(kullanıcılar_listesi), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Veritabanı tablolarını oluşturur
    app.run(debug=True)
