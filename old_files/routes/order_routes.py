from flask import Blueprint, request, jsonify
from app import db
from models.order import Order
from models.product import Product
from schemas.order_schema import OrderSchema
from schemas.product_schema import ProductSchema
from datetime import datetime

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
products_schema = ProductSchema(many=True)

@orders_bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    order_date = data.get('order_date')
    if order_date:
        order_date = datetime.fromisoformat(order_date)
    else:
        order_date = datetime.utcnow()
    new_order = Order(user_id=data['user_id'], order_date=order_date)
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 201

@orders_bp.route('/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
    if product in order.products:
        return jsonify({'message': 'Product already in order'}), 400
    order.products.append(product)
    db.session.commit()
    return jsonify({'message': 'Product added to order successfully'}), 200

@orders_bp.route('/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
    if product not in order.products:
        return jsonify({'message': 'Product not in order'}), 400
    order.products.remove(product)
    db.session.commit()
    return jsonify({'message': 'Product removed from order successfully'}), 200

@orders_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return orders_schema.jsonify(orders)

@orders_bp.route('/<int:order_id>/products', methods=['GET'])
def get_order_products(order_id):
    order = Order.query.get_or_404(order_id)
    return products_schema.jsonify(order.products)
