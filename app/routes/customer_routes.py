from flask import Blueprint, request, jsonify
from app.models import Musteri, Aktivite, Firsat  # Burada doğru model adlarını kullanın
from app import db
from app.utils import apply_pagination, apply_sorting, apply_filters

customer_bp = Blueprint('customers', __name__)

@customer_bp.route('/', methods=['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'isim', type=str)
    sort_order = request.args.get('sort_order', 'asc', type=str)
    
    filters = {}
    for key in request.args:
        if key not in ['page', 'per_page', 'sort_by', 'sort_order']:
            filters[key] = request.args.get(key, type=str)
    
    query = Musteri.query
    query = apply_filters(query, Musteri, filters)
    query = apply_sorting(query, sort_by, sort_order)
    query = apply_pagination(query, page, per_page)
    
    customers = query.all()
    total = Musteri.query.count()

    return jsonify({
        'customers': [customer.to_dict() for customer in customers],
        'total': total,
        'page': page,
        'per_page': per_page
    })

@customer_bp.route('/<string:id>', methods=['GET'])
def get_customer(id):
    customer = Musteri.query.get(id)
    if customer:
        return jsonify({"id": customer.id, "name": customer.isim, "email": customer.email})
    else:
        return jsonify({"error": "Customer not found"}), 404
