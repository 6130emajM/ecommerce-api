from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ecom_user:ikustustofoardni@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Association table
order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship('Product', secondary=order_product, lazy='subquery', backref=db.backref('orders', lazy=True))

# Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# USER ENDPOINTS
@app.route('/users', methods=['GET'])
def get_users():
    return users_schema.jsonify(User.query.all())

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return user_schema.jsonify(User.query.get_or_404(id))

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], address=data.get('address',''), email=data['email'])
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.address = data.get('address', user.address)
    user.email = data.get('email', user.email)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

# PRODUCT ENDPOINTS
@app.route('/products', methods=['GET'])
def get_products():
    return products_schema.jsonify(Product.query.all())

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    return product_schema.jsonify(Product.query.get_or_404(id))

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(product_name=data['product_name'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.product_name = data.get('product_name', product.product_name)
    product.price = data.get('price', product.price)
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

# ORDER ENDPOINTS
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order_date = datetime.fromisoformat(data['order_date']) if 'order_date' in data else datetime.utcnow()
    order = Order(user_id=data['user_id'], order_date=order_date)
    db.session.add(order)
    db.session.commit()
    return order_schema.jsonify(order), 201

@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
    if product in order.products:
        return jsonify({'message': 'Product already in order'}), 400
    order.products.append(product)
    db.session.commit()
    return jsonify({'message': 'Product added'}), 200

@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
    if product not in order.products:
        return jsonify({'message': 'Product not in order'}), 400
    order.products.remove(product)
    db.session.commit()
    return jsonify({'message': 'Product removed'}), 200

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    return orders_schema.jsonify(Order.query.filter_by(user_id=user_id).all())

@app.route('/orders/<int:order_id>/products', methods=['GET'])
def get_order_products(order_id):
    order = Order.query.get_or_404(order_id)
    return products_schema.jsonify(order.products)

with app.app_context():
    db.create_all()
    print("="*50)
    print("✅ DATABASE READY!")
    print("="*50)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
