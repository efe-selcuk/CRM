from flask import Blueprint, jsonify
from app.models import Satis
from app import db

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/sales')
def get_sales():
    sales = Satis.query.all()
    sale_list = [{"id": s.id, "customer_id": s.musteri_id, "date": s.tarih, "total_amount": s.toplam_tutar} for s in sales]
    return jsonify(sale_list)

@sales_bp.route('/sales/<string:id>')
def get_sale(id):
    sale = Satis.query.get(id)
    if sale:
        return jsonify({"id": sale.id, "customer_id": sale.musteri_id, "date": sale.tarih, "total_amount": sale.toplam_tutar})
    else:
        return jsonify({"error": "Sale not found"}), 404
