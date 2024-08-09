from flask import Blueprint, request, jsonify
from app.services.email_sender import send_opportunity_email

email_bp = Blueprint('email', __name__)

@email_bp.route('/send-opportunity-email', methods=['POST'])
def send_opportunity_email_route():
    data = request.get_json()
    email_address = data.get('email')
    if not email_address:
        return jsonify({'error': 'Email address is required'}), 400

    try:
        send_opportunity_email(email_address)
        return jsonify({'message': 'Opportunity email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
