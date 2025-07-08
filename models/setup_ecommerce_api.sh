#!/bin/bash

echo "📦 Creating project structure..."

mkdir -p ecommerce_project/models
mkdir -p ecommerce_project/schemas
cd ecommerce_project || exit

touch app.py db.py requirements.txt
touch models/__init__.py models/base.py models/user.py models/order.py models/product.py
touch schemas/__init__.py schemas/user_schema.py schemas/product_schema.py schemas/order_schema.py

echo "✅ Files and folders created."

echo "📄 Writing requirements..."
cat <<EOF > requirements.txt
Flask
Flask-SQLAlchemy
Flask-Marshmallow
marshmallow
marshmallow-sqlalchemy
mysql-connector-python
EOF

echo "📄 Writing db.py..."
cat <<EOF > db.py
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
EOF

echo "📄 Writing models/base.py..."
cat <<EOF > models/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
EOF

echo "📄 Writing models/user.py..."
cat <<EOF > models/user.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base import Base

class User(Base):
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")
EOF

echo "📄 Writing models/order.py..."
cat <<EOF > models/order.py
from datetime import datetime
from sqlalchemy import ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base import Base

order_products = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("app_orders.id"), primary_key=True),
    Column("product_id", ForeignKey("app_products.id"), primary_key=True)
)

class Order(Base):
    __tablename__ = "app_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="orders")
    order_products: Mapped[List["Product"]] = relationship(
        "Product",
        secondary=order_products,
        back_populates="product_orders"
    )
EOF

echo "📄 Writing models/product.py..."
cat <<EOF > models/product.py
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base import Base
from models.order import order_products

class Product(Base):
    __tablename__ = "app_products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    product_orders: Mapped[List["Order"]] = relationship(
        "Order",
        secondary=order_products,
        back_populates="order_products"
    )
EOF

echo "📄 Writing models/__init__.py..."
cat <<EOF > models/__init__.py
from .user import User
from .product import Product
from .order import Order, order_products
EOF

echo "📄 Writing schemas/user_schema.py..."
cat <<EOF > schemas/user_schema.py
from db import ma
from models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
EOF

echo "📄 Writing schemas/product_schema.py..."
cat <<EOF > schemas/product_schema.py
from db import ma
from models.product import Product

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
EOF

echo "📄 Writing schemas/order_schema.py..."
cat <<EOF > schemas/order_schema.py
from marshmallow import fields
from db import ma
from models.order import Order

class OrderSchema(ma.SQLAlchemyAutoSchema):
    user_id = fields.Int(required=True)

    class Meta:
        model = Order
        load_instance = True
        include_fk = True
        dump_only = ("id",)
EOF

echo "📄 Writing schemas/__init__.py..."
cat <<EOF > schemas/__init__.py
from .user_schema import UserSchema
from .product_schema import ProductSchema
from .order_schema import OrderSchema
EOF

echo "📄 Writing app.py..."
cat <<EOF > app.py
from flask import Flask, request, jsonify
from db import db, ma
from models import User, Product, Order, order_products
from models.base import Base
from schemas import UserSchema, ProductSchema, OrderSchema
from sqlalchemy import select
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:flaskuser:Indra@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@app.route("/users", methods=["POST"])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.add(user_data)
    db.session.commit()
    return user_schema.jsonify(user_data), 201

@app.route("/users", methods=["GET"])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    return users_schema.jsonify(users), 200

@app.route("/products", methods=["POST"])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.add(product_data)
    db.session.commit()
    return product_schema.jsonify(product_data), 201

@app.route("/orders", methods=["POST"])
def create_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.add(order_data)
    db.session.commit()
    return order_schema.jsonify(order_data), 201

if __name__ == "__main__":
    with app.app_context():
        Base.metadata.create_all(db.engine)
    app.run(debug=True)
EOF

echo "✅ Project files are ready."

echo "🐍 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🎉 Setup complete. To run the API:"
echo "1. source venv/bin/activate"
echo "2. python app.py"
