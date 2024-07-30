from flask import Blueprint, request, jsonify
from app.models import Urun
from app import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Urun.query.all()
    return jsonify([{'id': p.id, 'ad': p.ad, 'kategori': p.kategori, 'fiyat': p.fiyat, 'stok_miktari': p.stok_miktari} for p in products])

@product_bp.route('/products/<string:id>', methods=['GET'])
def get_product(id):
    product = Urun.query.get(id)
    if product:
        return jsonify({'id': product.id, 'ad': product.ad, 'kategori': product.kategori, 'fiyat': product.fiyat, 'stok_miktari': product.stok_miktari})
    else:
        return jsonify({'message': 'Product not found'}), 404

@product_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Urun(
        id=data['id'],
        ad=data['ad'],
        kategori=data['kategori'],
        fiyat=data['fiyat'],
        stok_miktari=data['stok_miktari']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@product_bp.route('/products/<string:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Urun.query.get(id)
    if product:
        product.ad = data['ad']
        product.kategori = data['kategori']
        product.fiyat = data['fiyat']
        product.stok_miktari = data['stok_miktari']
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    else:
        return jsonify({'message': 'Product not found'}), 404

@product_bp.route('/products/<string:id>', methods=['DELETE'])
def delete_product(id):
    product = Urun.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'message': 'Product not found'}), 404
