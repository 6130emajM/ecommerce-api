from ecommerce_api.db_setup import ma
from ecommerce_api.models.customer import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
