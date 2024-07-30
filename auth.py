from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, Kullanıcı

auth_bp = Blueprint('auth', __name__)
limiter = Limiter(key_func=get_remote_address)

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()

    required_fields = ['id', 'isim', 'email', 'şifre', 'rol']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"'{field}' alanı eksik!"}), 400

    hashed_password = generate_password_hash(data['şifre'], method='pbkdf2:sha256')
    new_user = Kullanıcı(
        id=data['id'],
        isim=data['isim'],
        email=data['email'],
        şifre=hashed_password,
        rol=data['rol']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Kullanıcı kaydedildi!"}), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    if 'email' not in data or 'şifre' not in data:
        return jsonify({"message": "E-posta ve şifre gerekli!"}), 400

    user = Kullanıcı.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.şifre, data['şifre']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Geçersiz e-posta veya şifre"}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
@limiter.limit("10 per minute")
def protected():
    return jsonify({"message": "Bu alana erişim yetkiniz var!"}), 200
