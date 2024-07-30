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
        return jsonify({"message": "Missing required fields"}), 400

    if Personel.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    new_personel = Personel(
        isim=isim,
        email=email,
        rol=rol
    )
    new_personel.set_password(sifre)
    db.session.add(new_personel)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Dakikada 10 istek limiti
def login():
    data = request.get_json()

    email = data.get('email')
    sifre = data.get('sifre')

    if not email or not sifre:
        return jsonify({"message": "Missing email or password"}), 400

    personel = Personel.query.filter_by(email=email).first()

    if personel is None or not personel.check_password(sifre):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity={'id': personel.id, 'rol': personel.rol})
    return jsonify(access_token=access_token), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
@limiter.limit("5 per minute")  # Dakikada 5 istek limiti
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
