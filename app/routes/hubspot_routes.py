import os
import requests
from flask import Blueprint, request, jsonify

hubspot_bp = Blueprint('hubspot', __name__)

# HubSpot API bilgileri
HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
HUBSPOT_API_URL = 'https://api.hubapi.com'

@hubspot_bp.route('/sync/customers', methods=['POST'])
def sync_customers():
    data = request.json

    # Veri kontrolü
    if not data or not isinstance(data, list) or not all(customer.get('email') for customer in data):
        return jsonify({"error": "Missing 'email' in request data"}), 400

    # Her müşteri için API isteği yapma
    responses = []
    for customer in data:
        email = customer.get('email')
        hubspot_endpoint = f'{HUBSPOT_API_URL}/contacts/v1/contact/createOrUpdate/email/{email}/?hapikey={HUBSPOT_API_KEY}'

        response = requests.post(hubspot_endpoint, json={
            "properties": [
                {"property": "firstname", "value": customer.get("isim")},
                {"property": "phone", "value": customer.get("telefon")},
                {"property": "address", "value": customer.get("adres")}
            ]
        })

        if response.status_code == 200:
            responses.append({"email": email, "status": "synced"})
        else:
            responses.append({
                "email": email,
                "status": "failed",
                "error": response.json().get('message', 'Unknown error')
            })

    return jsonify({"results": responses}), 200

@hubspot_bp.route('/authorize', methods=['GET'])
def authorize():
    # HubSpot authorization URL'ini döndür
    redirect_uri = os.getenv('REDIRECT_URI')
    hubspot_auth_url = (
        f'https://app.hubspot.com/oauth/authorize'
        f'?client_id={os.getenv("HUBSPOT_CLIENT_ID")}'
        f'&redirect_uri={redirect_uri}'
        f'&scope=contacts'
    )
    return jsonify({"url": hubspot_auth_url})

@hubspot_bp.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    redirect_uri = os.getenv('REDIRECT_URI')
    
    # Token almak için HubSpot'a istek yap
    token_endpoint = 'https://api.hubapi.com/oauth/v1/token'
    response = requests.post(token_endpoint, data={
        'grant_type': 'authorization_code',
        'client_id': os.getenv('HUBSPOT_CLIENT_ID'),
        'client_secret': os.getenv('HUBSPOT_CLIENT_SECRET'),
        'redirect_uri': redirect_uri,
        'code': code
    })
    
    if response.status_code == 200:
        token_data = response.json()
        # Token'ı işleme ve saklama
        return jsonify(token_data), 200
    else:
        return jsonify({"error": "Failed to get access token"}), response.status_code
