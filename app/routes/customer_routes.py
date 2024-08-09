from flask import Blueprint, request, jsonify
from app.models import Musteri
from app import db
from app.utils import apply_pagination, apply_sorting, apply_filters
import requests
import os

customer_bp = Blueprint('customers', __name__)

# HubSpot API bilgileri
HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
HUBSPOT_API_URL = 'https://api.hubapi.com'

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
        return jsonify({
            "id": customer.id,
            "name": customer.isim,
            "email": customer.email
        })
    else:
        return jsonify({"error": "Customer not found"}), 404

@customer_bp.route('/sync/customers', methods=['POST'])
def sync_customers():
    data = request.json
    # Eğer 'email' anahtarı eksikse hata döner
    if 'email' not in data:
        return jsonify({"error": "Missing 'email' in request data"}), 400

    hubspot_endpoint = f'{HUBSPOT_API_URL}/contacts/v1/contact/createOrUpdate/email/{data["email"]}/?hapikey={HUBSPOT_API_KEY}'
    response = requests.post(hubspot_endpoint, json={
        "properties": [
            {"property": "firstname", "value": data.get("firstname")},
            {"property": "lastname", "value": data.get("lastname")},
            {"property": "phone", "value": data.get("phone")}
        ]
    })

    if response.status_code == 200:
        return jsonify({"message": "Customer synced with HubSpot"}), 200
    else:
        return jsonify({"error": f"Failed to sync customer: {response.json().get('message') or 'Unknown error'}"}), response.status_code

print(f"HubSpot API Key: {HUBSPOT_API_KEY}")
