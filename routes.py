from app import app, db
from flask import request, jsonify
from models import Customer, Product, Order
from schemas import CustomerSchema, ProductSchema, OrderSchema

customer_schema = CustomerSchema()
product_schema = ProductSchema()
order_schema = OrderSchema()

@app.route('/')
def index():
    return {"message": "Welcome to the E-Commerce API!"}

# ----- Customers -----
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer)

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return customer_schema.jsonify(customers, many=True)

# ----- Products -----
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return product_schema.jsonify(products, many=True)

# ----- Orders -----
@app.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    new_order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order)

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return order_schema.jsonify(orders, many=True)
