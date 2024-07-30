# app/middlewares/roles.py

from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app import db
from app.models import Personel

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = Personel.query.get(current_user_id)
            if user and user.rol == required_role:
                return fn(*args, **kwargs)
            else:
                return {"msg": "Erişim reddedildi"}, 403
        return wrapper
    return decorator
