from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
