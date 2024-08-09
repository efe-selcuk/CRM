from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utils import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin-only', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_only():
    return jsonify({"message": "Welcome, admin!"}), 200
