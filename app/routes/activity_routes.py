from flask import Blueprint, jsonify
from app.models import Aktivite
from app import db

activity_bp = Blueprint('activities', __name__)

@activity_bp.route('/activities')
def get_activities():
    activities = Aktivite.query.all()
    activity_list = [{"id": a.id, "customer_id": a.musteri_id, "date": a.tarih, "type": a.tur, "note": a.not_} for a in activities]
    return jsonify(activity_list)

@activity_bp.route('/activities/<string:id>')
def get_activity(id):
    activity = Aktivite.query.get(id)
    if activity:
        return jsonify({"id": activity.id, "customer_id": activity.musteri_id, "date": activity.tarih, "type": activity.tur, "note": activity.not_})
    else:
        return jsonify({"error": "Activity not found"}), 404
