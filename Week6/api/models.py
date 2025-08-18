from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from .db import db


# Base Product
class Product(db.Model):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_name = Column(String(50), nullable=False)
    category = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    type = Column(String(20))  # Polymorphic identity
    __mapper_args__ = {"polymorphic_identity": "product", "polymorphic_on": type}

    def get_total_value(self):
        """
        Calculates the total value of the product based on its price and quantity.
        """
        return self.price * self.quantity


class FoodProduct(Product):
    __tablename__ = "food_products"
    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    mfg_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "food",
    }


class ElectronicProduct(Product):
    __tablename__ = "electronic_products"
    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    purchase_date = Column(DateTime, nullable=False)
    warranty_period = Column(Integer, nullable=False)  # months

    __mapper_args__ = {
        "polymorphic_identity": "electronic",
    }

    def get_warranty_end_date(self):
        return self.purchase_date + relativedelta(months=self.warranty_period)


class BookProduct(Product):
    __tablename__ = "book_products"
    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    author = Column(String(50), nullable=False)
    publication_year = Column(Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "book",
    }
