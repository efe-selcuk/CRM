from flask import Blueprint, request, jsonify
from app.models import Satis
from app import db
from app.utils import apply_pagination, apply_sorting, apply_filters

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/', methods=['GET'])
def get_sales():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'tarih', type=str)
    sort_order = request.args.get('sort_order', 'asc', type=str)
    
    filters = {}
    for key in request.args:
        if key not in ['page', 'per_page', 'sort_by', 'sort_order']:
            filters[key] = request.args.get(key, type=str)
    
    query = Satis.query
    query = apply_filters(query, Satis, filters)
    query = apply_sorting(query, sort_by, sort_order)
    query = apply_pagination(query, page, per_page)
    
    sales = query.all()
    total = Satis.query.count()

    return jsonify({
        'sales': [sale.to_dict() for sale in sales],
        'total': total,
        'page': page,
        'per_page': per_page
    })

@sales_bp.route('/sales/<string:id>', methods=['GET'])
def get_sale(id):
    sale = Satis.query.get(id)
    if sale:
        return jsonify({"id": sale.id, "customer_id": sale.musteri_id, "date": sale.tarih, "total_amount": sale.toplam_tutar})
    else:
        return jsonify({"error": "Sale not found"}), 404
