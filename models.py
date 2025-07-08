from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

class Customer(db.Model): ...
class Products(db.Model): ...
class Orders(db.Model): ...

