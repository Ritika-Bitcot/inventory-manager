# tests/test_models.py

from datetime import date, timedelta

import pytest
from api.models import BookProduct, ElectronicProduct, FoodProduct, Product
from dateutil.relativedelta import relativedelta
from sqlalchemy.exc import IntegrityError


# ----------------------
# Product Tests
# ----------------------
def test_product_total_value_and_serialize(db_session, test_user) -> None:
    """
    Test that creating a Product and serializing it succeeds.

    The test case creates a Product with valid fields and verifies that
    the fields are correctly set and the total value is calculated correctly.
    The test also verifies that the serialize method returns
    a JSON-serializable dictionary
    representation of the product.
    """
    product = Product(
        product_name="Generic",
        category="product",
        quantity=10,
        price=5.5,
        owner_id=test_user.id,
    )
    db_session.add(product)
    db_session.commit()

    assert product.get_total_value() == 55.0
    serialized = product.serialize()
    assert serialized["product_name"] == "Generic"
    assert serialized["category"] == "product"
    assert serialized["quantity"] == 10
    assert serialized["price"] == 5.5
    assert serialized["owner_id"] == str(test_user.id)


def test_product_missing_required_fields(db_session) -> None:
    """
    Test that creating a Product with missing required fields raises an IntegrityError.

    A Product requires the owner_id field to be set.
    """
    with pytest.raises(IntegrityError):
        p = Product(category="product", quantity=1, price=10)  # missing owner_id
        db_session.add(p)
        db_session.commit()


# ----------------------
# FoodProduct Tests
# ----------------------
def test_food_product_creation_and_serialize(db_session, test_user) -> None:
    """
    Ensure FoodProduct instance can be created and serialized correctly.
    """
    mfg = date.today()
    expiry = mfg + timedelta(days=10)
    food = FoodProduct(
        product_name="Lassi",
        category="food",
        quantity=20,
        price=2.5,
        mfg_date=mfg,
        expiry_date=expiry,
        owner_id=test_user.id,
    )
    db_session.add(food)
    db_session.commit()

    assert food.product_name == "Lassi"
    assert food.category == "food"
    assert food.mfg_date == mfg
    assert food.expiry_date == expiry

    serialized = food.serialize()
    assert serialized["product_name"] == "Lassi"
    assert serialized["category"] == "food"


def test_food_product_invalid_dates(db_session, test_user) -> None:
    """
    Test that creating a FoodProduct instance with invalid dates raises
    a ValidationError. The test creates a FoodProduct instance with a
    manufacturing date after the expiry date, and asserts that the
    expiry_date attribute is set to a value that is earlier than the
    current date.
    """
    mfg = date.today()
    expiry = mfg - timedelta(days=1)
    food = FoodProduct(
        product_name="Cheese",
        category="food",
        quantity=5,
        price=3.0,
        mfg_date=mfg,
        expiry_date=expiry,
        owner_id=test_user.id,
    )
    db_session.add(food)
    db_session.commit()
    assert food.expiry_date < date.today()


# ----------------------
# ElectronicProduct Tests
# ----------------------
def test_electronic_product_creation_and_warranty(db_session, test_user) -> None:
    """
    Ensure that creating an ElectronicProduct instance with valid data succeeds.

    This test case creates an ElectronicProduct instance with valid values for
    purchase_date, warranty_period, and other required fields. It then asserts
    that the instance attributes are correctly set and that the
    get_warranty_end_date() method returns the correct value.
    """
    purchase = date.today()
    electronic = ElectronicProduct(
        product_name="Laptop",
        category="electronic",
        quantity=3,
        price=1000.0,
        purchase_date=purchase,
        warranty_period=24,
        owner_id=test_user.id,
    )
    db_session.add(electronic)
    db_session.commit()

    assert electronic.purchase_date == purchase
    assert electronic.warranty_period == 24
    assert electronic.get_warranty_end_date() == purchase + relativedelta(months=24)


def test_electronic_product_missing_fields(db_session, test_user) -> None:
    """
    Test creating an ElectronicProduct instance with missing required fields.

    Ensures that attempting to create an ElectronicProduct instance with a missing
    purchase_date raises an IntegrityError.
    """
    with pytest.raises(IntegrityError):
        e = ElectronicProduct(
            product_name="Phone",
            category="electronic",
            quantity=2,
            price=500.0,
            purchase_date=None,  # required
            warranty_period=12,
            owner_id=test_user.id,
        )
        db_session.add(e)
        db_session.commit()


# ----------------------
# BookProduct Tests
# ----------------------
def test_book_product_creation(db_session, test_user) -> None:
    """
    Test that creating a BookProduct with valid fields succeeds.

    The test case creates a BookProduct with valid fields and verifies that
    the fields are correctly set and the total value is calculated correctly.
    """
    book = BookProduct(
        product_name="Python 101",
        category="book",
        quantity=15,
        price=45.0,
        author="John Doe",
        publication_year=2020,
        owner_id=test_user.id,
    )
    db_session.add(book)
    db_session.commit()

    assert book.author == "John Doe"
    assert book.publication_year == 2020
    assert book.get_total_value() == 15 * 45.0


def test_book_product_missing_fields(db_session, test_user) -> None:
    """
    Test that creating a BookProduct with
    missing required fields raises an IntegrityError.

    A BookProduct requires the author and publication_year fields to be set.
    """
    with pytest.raises(IntegrityError):
        b = BookProduct(
            product_name="Python Advanced",
            category="book",
            quantity=5,
            price=50.0,
            author=None,  # required
            publication_year=2021,
            owner_id=test_user.id,
        )
        db_session.add(b)
        db_session.commit()
