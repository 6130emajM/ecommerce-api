from flask_marshmallow import Marshmallow
from models import Customer, Order, Product

ma = Marshmallow()

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_relationships = True
        load_instance = True
    products = ma.Nested(ProductSchema, many=True)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_relationships = True
        load_instance = True
    orders = ma.Nested(OrderSchema, many=True)
