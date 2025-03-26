from flask import Blueprint, request, jsonify
from models import Product
from db import db
from flask_jwt_extended import jwt_required

product_blueprint = Blueprint('products', __name__)

@product_blueprint.route('/', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data.get('stock', 0)
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(message="added successfully"), 201

@product_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    output = [{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price, 'stock': p.stock}
              for p in products]
    return jsonify(products=output)

@product_blueprint.route('/<int:pid>', methods=['PUT'])
@jwt_required()
def update_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify(message="not founded"), 404

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)

    db.session.commit()
    return jsonify(message="updated successfully")

@product_blueprint.route('/<int:pid>', methods=['DELETE'])
@jwt_required()
def delete_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify(message="not founded"), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify(message="deleted successfully")
