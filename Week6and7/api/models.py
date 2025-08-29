import uuid

from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from .db import db


# Base Product
class Product(db.Model):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_name = Column(String(50), nullable=False)
    category = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": category,
        "polymorphic_identity": "product",
    }
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    def get_total_value(self):
        """
        Calculates the total value of the product based on its price and quantity.
        """
        return self.price * self.quantity

    def serialize(self):
        """
        Returns a JSON serializable representation of the product.

        Returns:
        A dictionary that can be serialized to JSON.
        """
        return {
            "id": self.id,
            "product_name": self.product_name,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price,
            "owner_id": self.owner_id,
        }


class FoodProduct(Product):
    __tablename__ = "food_products"
    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    mfg_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "food",
    }

    def __init__(
        self, product_name, category, quantity, price, mfg_date, expiry_date, owner_id
    ) -> None:
        """
        Initializes a FoodProduct instance with the given arguments.

        Args:
            product_name (str): The name of the product.
            category (str): The category of the product.
            quantity (int): The quantity of the product.
            price (float): The price of the product.
            mfg_date (Date): The manufacturing date of the product.
            expiry_date (Date): The expiry date of the product.
        """
        super().__init__(
            product_name=product_name,
            category=category,
            quantity=quantity,
            price=price,
            owner_id=owner_id,
        )
        self.mfg_date = mfg_date
        self.expiry_date = expiry_date


class ElectronicProduct(Product):
    __tablename__ = "electronic_products"
    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    purchase_date = Column(Date, nullable=False)
    warranty_period = Column(Integer, nullable=False)  # months

    __mapper_args__ = {
        "polymorphic_identity": "electronic",
    }

    def __init__(
        self,
        product_name,
        category,
        quantity,
        price,
        purchase_date,
        warranty_period,
        owner_id,
    ) -> None:
        """
        Initializes an ElectronicProduct instance with the given arguments.

        Args:
            product_name (str): The name of the product.
            category (str): The category of the product.
            quantity (int): The quantity of the product.
            price (float): The price of the product.
            purchase_date (Date): The purchase date of the product.
            warranty_period (int): The warranty period in months.
        """
        super().__init__(
            product_name=product_name,
            category=category,
            quantity=quantity,
            price=price,
            owner_id=owner_id,
        )
        self.purchase_date = purchase_date
        self.warranty_period = warranty_period

    def get_warranty_end_date(self):
        """
        Calculates the warranty end date based on the purchase date.

        Returns:
            Date: The warranty end date.
        """
        return self.purchase_date + relativedelta(months=self.warranty_period)


class BookProduct(Product):
    __tablename__ = "book_products"
    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    author = Column(String(50), nullable=False)
    publication_year = Column(Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "book",
    }

    def __init__(
        self,
        product_name,
        category,
        quantity,
        price,
        author,
        publication_year,
        owner_id,
    ) -> None:
        """
        Initializes a BookProduct instance with the given arguments.

        Args:
            product_name (str): The name of the product.
            category (str): The category of the product.
            quantity (int): The quantity of the product.
            price (float): The price of the product.
            author (str): The author of the book.
            publication_year (int): The year of publication.
        """
        super().__init__(
            product_name=product_name,
            category=category,
            quantity=quantity,
            price=price,
            owner_id=owner_id,
        )
        self.author = author
        self.publication_year = publication_year


class User(db.Model):
    """
    Represents a user in the system.
    """

    __tablename__ = "users"

    ROLE_CHOICES = ("staff", "manager", "admin")

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        Enum(*ROLE_CHOICES, name="user_roles", create_type=True),
        nullable=False,
        default="staff",
    )

    def set_password(self, password: str) -> None:
        """
        Hash and set the user's password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verify a plaintext password against the stored hash.
        """
        return check_password_hash(self.password_hash, password)

    def serialize(self) -> dict:
        """
        Return a safe dict representation of the user.
        """
        return {
            "id": str(self.id),
            "username": self.username,
        }
