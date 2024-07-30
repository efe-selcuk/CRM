from flask import Blueprint, request, jsonify
from app.models import Urun
from app import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Urun.query.all()
    # Kategori gibi ilişkili nesnelerin JSON'a dönüştürülmesi gerekebilir
    return jsonify([{
        'id': p.id,
        'ad': p.ad,
        'kategori': p.kategori.ad if p.kategori else None,  # Kategori nesnesini JSON'a dönüştür
        'fiyat': p.fiyat,
        'stok_miktari': p.stok_miktari
    } for p in products])

@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Urun.query.get(id)
    if product:
        return jsonify({
            'id': product.id,
            'ad': product.ad,
            'kategori': product.kategori.ad if product.kategori else None,  # Kategori nesnesini JSON'a dönüştür
            'fiyat': product.fiyat,
            'stok_miktari': product.stok_miktari
        })
    else:
        return jsonify({'message': 'Product not found'}), 404

@product_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    
    # id'nin otomatik artmasını sağlamak için id'nin verilmemesi daha iyi olabilir
    new_product = Urun(
        ad=data['ad'],
        kategori=data.get('kategori'),  # Kategori, opsiyonel bir alan olabilir
        fiyat=data['fiyat'],
        stok_miktari=data['stok_miktari']
    )
    
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@product_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Urun.query.get(id)
    
    if product:
        product.ad = data.get('ad', product.ad)
        product.kategori = data.get('kategori', product.kategori)
        product.fiyat = data.get('fiyat', product.fiyat)
        product.stok_miktari = data.get('stok_miktari', product.stok_miktari)
        
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    else:
        return jsonify({'message': 'Product not found'}), 404

@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Urun.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'message': 'Product not found'}), 404
