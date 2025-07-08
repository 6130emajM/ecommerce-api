from ecommerce_api.db_setup import ma
from ecommerce_api.models.product import Product

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
