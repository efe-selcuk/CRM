from flask import Blueprint, jsonify
from app.models import Musteri

satis_tahmini_bp = Blueprint('satis_tahmini_bp', __name__)

@satis_tahmini_bp.route('/satis-tahmini', methods=['GET'])
def satis_tahmini():
    musteriler = Musteri.query.all()

    if not musteriler:
        return jsonify({"error": "No customer data available"}), 404

    sadakat_puanlari = [musteri.sadakat_puani for musteri in musteriler]
    alisveris_sikliklari = [musteri.alisveris_sikligi for musteri in musteriler]

    ortalama_sadakat_puani = sum(sadakat_puanlari) / len(sadakat_puanlari)
    ortalama_alisveris_sikligi = sum(alisveris_sikliklari) / len(alisveris_sikliklari)

    tahmin = (ortalama_sadakat_puani * 0.5) + (ortalama_alisveris_sikligi * 0.3)

    durum = "Satışlar artacak" if tahmin > 50 else "Satışlar azalacak"

    return jsonify({"tahmin": tahmin, "durum": durum})
