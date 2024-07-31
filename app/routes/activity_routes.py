from flask import Blueprint, request, jsonify
from app.models import Aktivite
from app import db
from app.utils import apply_pagination, apply_sorting, apply_filters

activity_bp = Blueprint('activities', __name__)

@activity_bp.route('/', methods=['GET'])
def get_activities():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'tarih', type=str)
    sort_order = request.args.get('sort_order', 'asc', type=str)
    
    filters = {}
    for key in request.args:
        if key not in ['page', 'per_page', 'sort_by', 'sort_order']:
            filters[key] = request.args.get(key, type=str)
    
    query = Aktivite.query
    query = apply_filters(query, Aktivite, filters)
    query = apply_sorting(query, sort_by, sort_order)
    query = apply_pagination(query, page, per_page)
    
    activities = query.all()
    total = Aktivite.query.count()

    return jsonify({
        'activities': [activity.to_dict() for activity in activities],
        'total': total,
        'page': page,
        'per_page': per_page
    })

@activity_bp.route('/activities/<string:id>', methods=['GET'])
def get_activity(id):
    activity = Aktivite.query.get(id)
    if activity:
        return jsonify({"id": activity.id, "customer_id": activity.musteri_id, "date": activity.tarih, "type": activity.tur, "note": activity.not_})
    else:
        return jsonify({"error": "Activity not found"}), 404
