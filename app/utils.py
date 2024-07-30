from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models import Personel

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = Personel.query.filter_by(id=current_user_id).first()
            if current_user is None or current_user.rol != required_role:
                return jsonify({"msg": "You do not have access to this resource"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
