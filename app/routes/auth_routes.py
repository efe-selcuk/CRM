from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, limiter
from app.models import Personel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")  # Dakikada 5 istek limiti
def register():
    data = request.get_json()

    isim = data.get('isim')
    email = data.get('email')
    sifre = data.get('sifre')
    rol = data.get('rol')

    if not all([isim, email, sifre, rol]):
        return jsonify({"message": "Eksik alanlar mevcut"}), 400

    if Personel.query.filter_by(email=email).first():
        return jsonify({"message": "Email zaten mevcut"}), 400

    new_personel = Personel(
        isim=isim,
        email=email,
        rol=rol
    )
    new_personel.set_password(sifre)
    db.session.add(new_personel)
    db.session.commit()

    return jsonify({"message": "Kullanıcı başarıyla kayıt edildi"}), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Dakikada 10 istek limiti
def login():
    data = request.get_json()

    email = data.get('email')
    sifre = data.get('sifre')

    if not email or not sifre:
        return jsonify({"message": "Email veya şifre eksik"}), 400

    personel = Personel.query.filter_by(email=email).first()

    if personel is None or not personel.check_password(sifre):
        return jsonify({"message": "Geçersiz kimlik bilgileri"}), 401

    access_token = create_access_token(identity={'id': personel.id, 'rol': personel.rol})
    return jsonify(access_token=access_token), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email eksik"}), 400

    personel = Personel.query.filter_by(email=email).first()
    if personel is None:
        return jsonify({"message": "Email bulunamadı"}), 404

    # Şifre sıfırlama işlemi burada yapılmalıdır.
    # Örneğin, bir sıfırlama bağlantısı veya şifre sıfırlama talimatı gönderilmelidir.
    # Bu işlem genellikle bir e-posta yoluyla yapılır.

    return jsonify({"message": "Şifre sıfırlama talimatı gönderildi"}), 200
