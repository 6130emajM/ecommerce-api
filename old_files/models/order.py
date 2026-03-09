from app import db
from datetime import datetime
from models.order_product import order_product

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship('Product', secondary=order_product, lazy='subquery', backref=db.backref('orders', lazy=True))
