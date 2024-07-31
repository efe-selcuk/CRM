# app/utils.py
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from app.models import Personel

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = Personel.query.filter_by(id=current_user_id['id']).first()
            if current_user is None or current_user.rol != required_role:
                return jsonify({"msg": "You do not have access to this resource"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator



def apply_pagination(query, page, per_page):
    return query.offset((page - 1) * per_page).limit(per_page)

def apply_sorting(query, model, sort_by=None, sort_order='asc'):
    if sort_by and sort_order:
        column = getattr(model, sort_by, None)
        if column:
            if sort_order.lower() == 'asc':
                query = query.order_by(column.asc())
            elif sort_order.lower() == 'desc':
                query = query.order_by(column.desc())
    return query

def apply_filters(query, model, filters):
    for key, value in filters.items():
        column = getattr(model, key, None)
        if column:
            if isinstance(value, str):
                query = query.filter(column.like(f'%{value}%'))
            else:
                query = query.filter(column == value)
    return query
