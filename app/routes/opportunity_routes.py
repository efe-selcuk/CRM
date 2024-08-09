from flask import Blueprint, request, jsonify
from app.models import Firsat
from app import db
from app.utils import apply_pagination, apply_sorting, apply_filters

opportunity_bp = Blueprint('opportunities', __name__)

@opportunity_bp.route('/', methods=['GET'])
def get_opportunities():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'start_date', type=str)
    sort_order = request.args.get('sort_order', 'asc', type=str)
    
    filters = {}
    for key in request.args:
        if key not in ['page', 'per_page', 'sort_by', 'sort_order']:
            filters[key] = request.args.get(key, type=str)
    
    query = Firsat.query
    query = apply_filters(query, Firsat, filters)
    query = apply_sorting(query, sort_by, sort_order)
    query = apply_pagination(query, page, per_page)
    
    opportunities = query.all()
    total = Firsat.query.count()

    return jsonify({
        'opportunities': [opportunity.to_dict() for opportunity in opportunities],
        'total': total,
        'page': page,
        'per_page': per_page
    })

@opportunity_bp.route('/<string:id>', methods=['GET'])
def get_opportunity(id):
    opportunity = Firsat.query.get(id)
    if opportunity:
        return jsonify({
            "id": opportunity.id,
            "product_id": opportunity.urun_id,
            "discount": opportunity.indirim,
            "start_date": opportunity.baslangic_tarihi.strftime('%Y-%m-%d'),
            "end_date": opportunity.bitis_tarihi.strftime('%Y-%m-%d')
        })
    else:
        return jsonify({"error": "Opportunity not found"}), 404
