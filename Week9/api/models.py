import uuid
from datetime import datetime, timedelta, timezone

from dateutil.relativedelta import relativedelta
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
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

    def get_total_value(self) -> float:
        """Calculate the total value of the product (price * quantity)."""
        return self.price * self.quantity

    def serialize(self) -> dict:
        """Return a JSON-serializable dictionary representation of the product."""
        return {
            "id": self.id,
            "product_name": self.product_name,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price,
            "owner_id": str(self.owner_id),
        }


class FoodProduct(Product):
    __tablename__ = "food_products"

    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    mfg_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "food"}

    def __init__(
        self, product_name, category, quantity, price, mfg_date, expiry_date, owner_id
    ) -> None:
        """
        Initialize a FoodProduct instance.
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

    __mapper_args__ = {"polymorphic_identity": "electronic"}

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
        Initialize an ElectronicProduct instance.
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

    def get_warranty_end_date(self) -> Date:
        """Calculate warranty end date using
        purchase_date + warranty_period (months)."""
        return self.purchase_date + relativedelta(months=self.warranty_period)


class BookProduct(Product):
    __tablename__ = "book_products"

    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    author = Column(String(50), nullable=False)
    publication_year = Column(Integer, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "book"}

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
        Initialize a BookProduct instance.
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
        Enum(*ROLE_CHOICES, name="user_roles"),
        nullable=False,
        default="staff",
    )

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def serialize(self) -> dict:
        """Return a safe dict representation of the user (excluding password)."""
        return {
            "id": str(self.id),
            "username": self.username,
            "role": self.role,
        }


class LLMCache(db.Model):
    __tablename__ = "llm_cache"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    model = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )
    expires_at = Column(
        DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(hours=1)
    )

    def is_expired(self) -> bool:
        """Check if this cache entry is expired."""
        return datetime.now(timezone.utc) >= self.expires_at


class Document(db.Model):
    __tablename__ = "user_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True
    )
    visibility = Column(
        String(32), nullable=False, default="user"
    )  # 'user' or 'global'
    content_type = Column(String(64), nullable=True)
    size = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def serialize(self) -> dict:
        """Return metadata about the document (not the content)."""
        return {
            "id": self.id,
            "filename": self.filename,
            "owner_id": str(self.owner_id) if self.owner_id else None,
            "visibility": self.visibility,
            "content_type": self.content_type,
            "size": self.size,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
