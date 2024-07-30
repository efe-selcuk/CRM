from flask import Blueprint, request, jsonify
from app.models import Musteri
from app import db

satis_tahmini_bp = Blueprint('satis_tahmini_bp', __name__)

@satis_tahmini_bp.route('/satis-tahmini', methods=['GET'])
def satis_tahmini():
    # Tüm müşteri verilerini al
    musteriler = Musteri.query.all()

    if not musteriler:
        return jsonify({"error": "No customer data available"}), 404

    # Müşteri sadakat puanı ve alışveriş sıklığını toplamak için listeler
    sadakat_puanlari = [musteri.sadakat_puani for musteri in musteriler]
    alisveris_sikliklari = [musteri.alisveris_sikligi for musteri in musteriler]

    # Genel ortalamaları hesapla
    ortalama_sadakat_puani = sum(sadakat_puanlari) / len(sadakat_puanlari)
    ortalama_alisveris_sikligi = sum(alisveris_sikliklari) / len(alisveris_sikliklari)

    # Basit bir tahmin hesaplama
    tahmin = (ortalama_sadakat_puani * 0.5) + (ortalama_alisveris_sikligi * 0.3)

    # Satışların artış veya azalış göstereceğini belirle
    if tahmin > 50:  # Örneğin, 50'nin üzerindeki tahminler artış olarak kabul edilebilir
        durum = "Satışlar artacak"
    else:
        durum = "Satışlar azalacak"

    return jsonify({"tahmin": tahmin, "durum": durum})
