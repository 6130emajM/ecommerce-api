from db import db

class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)

    order = db.relationship('Order', back_populates='products')
    product = db.relationship('Product', back_populates='order_products')
