from flask import Blueprint, request, jsonify
from app.models import Urun
from app import db
from app.utils import apply_pagination, apply_sorting, apply_filters

product_bp = Blueprint('products', __name__)

@product_bp.route('/', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'ad', type=str)
    sort_order = request.args.get('sort_order', 'asc', type=str)
    
    filters = {}
    for key in request.args:
        if key not in ['page', 'per_page', 'sort_by', 'sort_order']:
            filters[key] = request.args.get(key, type=str)
    
    query = Urun.query
    query = apply_filters(query, Urun, filters)
    query = apply_sorting(query, sort_by, sort_order)
    query = apply_pagination(query, page, per_page)
    
    products = query.all()
    total = Urun.query.count()

    return jsonify({
        'products': [product.to_dict() for product in products],
        'total': total,
        'page': page,
        'per_page': per_page
    })

@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Urun.query.get(id)
    if product:
        return jsonify({
            'id': product.id,
            'ad': product.ad,
            'kategori': product.kategori.ad if product.kategori else None,
            'fiyat': product.fiyat,
            'stok_miktari': product.stok_miktari
        })
    else:
        return jsonify({'message': 'Product not found'}), 404

@product_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Urun(
        ad=data['ad'],
        kategori=data.get('kategori'),
        fiyat=data['fiyat'],
        stok_miktari=data['stok_miktari']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@product_bp.route('/<int:id>', methods=['PUT'])
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

@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Urun.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'message': 'Product not found'}), 404
