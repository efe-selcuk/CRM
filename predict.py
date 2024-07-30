# predict.py
from flask import Blueprint, request, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from models import db, Müşteri, Satış

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/sales-forecast', methods=['POST'])
def sales_forecast():
    try:
        # Veritabanından müşteri ve satış verilerini al
        customers = Müşteri.query.all()
        sales = Satış.query.all()
        
        # Boş veri kontrolü
        if not customers or not sales:
            return jsonify({"error": "Yetersiz veri"}), 400
        
        # Veriyi DataFrame'e dönüştür
        customer_data = [{
            'id': customer.id,
            'alışveriş_sıklığı': customer.alışveriş_sıklığı,
            'sadakat_puanı': customer.sadakat_puanı
        } for customer in customers]
        sales_data = [{
            'müşteri_id': sale.müşteri_id,
            'toplam_tutar': sale.toplam_tutar
        } for sale in sales]

        df_customers = pd.DataFrame(customer_data)
        df_sales = pd.DataFrame(sales_data)
        
        # Satış verilerini müşteri verileri ile birleştir
        df = pd.merge(df_sales, df_customers, left_on='müşteri_id', right_on='id')
        
        # Özellikler ve hedef değişken
        X = df[['alışveriş_sıklığı', 'sadakat_puanı']]
        y = df['toplam_tutar']
        
        # Eğitim ve test setlerine ayır
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Regresyon modelini oluştur ve eğit
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Tüm müşteriler için tahmin yap
        all_customers = pd.DataFrame(customer_data)
        predictions = model.predict(all_customers[['alışveriş_sıklığı', 'sadakat_puanı']])
        
        # Ortalama tahmin sonucu
        avg_prediction = predictions.mean()

        # Genel satış analizi
        total_sales = df_sales['toplam_tutar'].sum()
        average_sales = df_sales['toplam_tutar'].mean()
        max_sales = df_sales['toplam_tutar'].max()
        min_sales = df_sales['toplam_tutar'].min()
        sales_count = df_sales.shape[0]

        return jsonify({
            "forecast": avg_prediction,
            "general_sales_analysis": {
                "total_sales": total_sales,
                "average_sales": average_sales,
                "max_sales": max_sales,
                "min_sales": min_sales,
                "sales_count": sales_count
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
