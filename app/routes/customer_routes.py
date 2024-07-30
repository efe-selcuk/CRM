from flask import Blueprint, jsonify
from app.models import Musteri
from app import db

customer_bp = Blueprint('customers', __name__)

@customer_bp.route('/customers')
def get_customers():
    customers = Musteri.query.all()
    customer_list = [{"id": c.id, "name": c.isim, "email": c.email} for c in customers]
    return jsonify(customer_list)

@customer_bp.route('/customers/<string:id>')
def get_customer(id):
    customer = Musteri.query.get(id)
    if customer:
        return jsonify({"id": customer.id, "name": customer.isim, "email": customer.email})
    else:
        return jsonify({"error": "Customer not found"}), 404
