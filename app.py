# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

# ===============================
# Fix IntegrityError import for Pylance
# ===============================
try:
    from sqlalchemy import IntegrityError
except ImportError:
    IntegrityError = Exception

# ===============================
# 1️⃣ App and Database Setup
# ===============================
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI',
    'mysql+pymysql://ecom_user:ikustustofoardni@localhost/ecommerce_api'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# ===============================
# 2️⃣ Association Table (Many-to-Many)
# ===============================
order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

# ===============================
# 3️⃣ Database Models
# ===============================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True, nullable=False)

    orders = db.relationship(
        'Order',
        backref='user',  # ✅ FIXED
        lazy=True,
        cascade='all, delete-orphan'
    )

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    products = db.relationship(
        'Product',
        secondary=order_product,
        lazy='subquery',
        backref=db.backref('orders', lazy=True)  # ✅ FIXED
    )

# ===============================
# 4️⃣ Marshmallow Schemas
# ===============================
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    products = ma.Nested(ProductSchema, many=True)
    class Meta:
        model = Order
        include_fk = True
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# ===============================
# 5️⃣ User Endpoints
# ===============================
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({
        "message": "Users retrieved successfully",
        "users": users_schema.dump(users)
    })

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        "message": "User retrieved successfully",
        "user": user_schema.dump(user)
    })

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400

    user = User(
        name=data['name'],
        address=data.get('address'),
        email=data['email']
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 400

    return jsonify({
        "message": "User created successfully",
        "user": user_schema.dump(user)
    }), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json

    user.name = data.get('name', user.name)
    user.address = data.get('address', user.address)
    user.email = data.get('email', user.email)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 400

    return jsonify({
        "message": "User updated successfully",
        "user": user_schema.dump(user)
    })

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# ===============================
# 6️⃣ Product Endpoints
# ===============================
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify({
        "message": "Products retrieved successfully",
        "products": products_schema.dump(products)
    })

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        "message": "Product retrieved successfully",
        "product": product_schema.dump(product)
    })

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json

    if not data or 'product_name' not in data or 'price' not in data:
        return jsonify({"error": "Product name and price are required"}), 400

    try:
        price = float(data['price'])
    except ValueError:
        return jsonify({"error": "Price must be a number"}), 400

    if price < 0:
        return jsonify({"error": "Price cannot be negative"}), 400

    product = Product(
        product_name=data['product_name'],
        price=price
    )

    db.session.add(product)
    db.session.commit()
    return jsonify({
        "message": "Product created successfully",
        "product": product_schema.dump(product)
    }), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json

    product.product_name = data.get('product_name', product.product_name)
    if 'price' in data:
        try:
            price = float(data['price'])
            if price < 0:
                return jsonify({"error": "Price cannot be negative"}), 400
            product.price = price
        except ValueError:
            return jsonify({"error": "Price must be a number"}), 400

    db.session.commit()
    return jsonify({
        "message": "Product updated successfully",
        "product": product_schema.dump(product)
    })

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})


# ===============================
# 8️⃣ Initialize Database & Run
# ===============================
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

