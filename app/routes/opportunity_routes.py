from flask import Blueprint, jsonify
from app.models import Firsat
from app import db

opportunity_bp = Blueprint('opportunities', __name__)

@opportunity_bp.route('/opportunities')
def get_opportunities():
    opportunities = Firsat.query.all()
    opportunity_list = [{"id": o.id, "product_id": o.urun_id, "discount": o.indirim, "start_date": o.baslangic_tarihi, "end_date": o.bitis_tarihi} for o in opportunities]
    return jsonify(opportunity_list)

@opportunity_bp.route('/opportunities/<string:id>')
def get_opportunity(id):
    opportunity = Firsat.query.get(id)
    if opportunity:
        return jsonify({"id": opportunity.id, "product_id": opportunity.urun_id, "discount": opportunity.indirim, "start_date": opportunity.baslangic_tarihi, "end_date": opportunity.bitis_tarihi})
    else:
        return jsonify({"error": "Opportunity not found"}), 404
