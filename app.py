from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Güvenli bir anahtar belirleyin
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)  # Token süresi
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Bellek içi depolama yapılandırması
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]  # Günlük ve saatlik limitler
)

class Müşteri(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    isim = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    telefon = db.Column(db.String(20))
    adres = db.Column(db.String(255))
    şirket = db.Column(db.String(100))

class Fırsat(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    müşteri_id = db.Column(db.String(36), db.ForeignKey('müşteri.id'), nullable=False)
    başlangıç_tarihi = db.Column(db.DateTime)
    bitiş_tarihi = db.Column(db.DateTime)
    aşama = db.Column(db.String(50))
    toplam_tutar = db.Column(db.Float)
    açıklama = db.Column(db.String(255))

class Aktivite(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    müşteri_id = db.Column(db.String(36), db.ForeignKey('müşteri.id'), nullable=False)
    tarih = db.Column(db.DateTime)
    tür = db.Column(db.String(50))
    not_ = db.Column(db.String(255))  # 'not' yerine 'not_' kullanıyoruz
    sonuç = db.Column(db.String(50))

class Kullanıcı(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    isim = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    şifre = db.Column(db.String(255), nullable=False)  # nullable=False ekledik
    rol = db.Column(db.String(50))

@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")  # Her dakikada 5 istek limiti
def register():
    data = request.get_json()

    # Verilerin doğruluğunu kontrol et
    required_fields = ['id', 'isim', 'email', 'şifre', 'rol']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"'{field}' alanı eksik!"}), 400

    hashed_password = generate_password_hash(data['şifre'], method='pbkdf2:sha256')  # Daha güvenli bir hash yöntemi
    new_user = Kullanıcı(
        id=data['id'],
        isim=data['isim'],
        email=data['email'],
        şifre=hashed_password,  # Hash'lenmiş şifreyi kaydediyoruz
        rol=data['rol']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Kullanıcı kaydedildi!"}), 201

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Her dakikada 5 istek limiti
def login():
    data = request.get_json()
    
    # Verilerin doğruluğunu kontrol et
    if 'email' not in data or 'şifre' not in data:
        return jsonify({"message": "E-posta ve şifre gerekli!"}), 400

    user = Kullanıcı.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.şifre, data['şifre']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Geçersiz e-posta veya şifre"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
@limiter.limit("10 per minute")  # Her dakikada 10 istek limiti
def protected():
    return jsonify({"message": "Bu alana erişim yetkiniz var!"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Veritabanı tablolarını oluşturur
    app.run(debug=True)
