from ecommerce_api.db_setup import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', backref='product', lazy=True)
