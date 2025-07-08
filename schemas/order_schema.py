from ecommerce_api.db_setup import ma
from ecommerce_api.models.order import Order

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
