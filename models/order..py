from sqlalchemy import ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

from ecommerce_api.models.user import User

from .base import Base
from .product import Product

order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("app_orders.id"), primary_key=True),
    Column("product_id", ForeignKey("app_products.id"), primary_key=True)
)

class Order(Base):
    __tablename__ = "app_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="orders")

    order_products: Mapped[List["Product"]] = relationship(
        "Product",
        secondary=order_product,
        back_populates="product_orders"
    )

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

