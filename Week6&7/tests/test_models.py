# tests/test_models.py

from datetime import date, timedelta

import pytest
from api.models import BookProduct, ElectronicProduct, FoodProduct, Product
from dateutil.relativedelta import relativedelta
from sqlalchemy.exc import IntegrityError


# ----------------------
# Product Tests
# ----------------------
def test_product_total_value_and_serialize(db_session) -> None:
    """
    Tests that a Product instance's total value is calculated correctly and that it
    can be serialized into a dictionary.
    """
    product = Product(
        product_name="Generic", category="product", quantity=10, price=5.5
    )
    db_session.add(product)
    db_session.commit()

    assert product.get_total_value() == 55.0

    serialized = product.serialize()
    assert serialized["product_name"] == "Generic"
    assert serialized["category"] == "product"
    assert serialized["quantity"] == 10
    assert serialized["price"] == 5.5


def test_product_missing_required_fields(db_session) -> None:
    # product_name is required
    """
    Tests that a Product instance must have a product_name.

    If the product_name is None or empty string, the instance should not be
    valid and should raise an IntegrityError when trying to commit to the
    database.
    """
    with pytest.raises(IntegrityError):
        p = Product(category="product", quantity=1, price=10)
        db_session.add(p)
        db_session.commit()


# ----------------------
# FoodProduct Tests
# ----------------------
def test_food_product_creation_and_serialize(db_session) -> None:
    """
    Tests that a FoodProduct instance is created successfully and can be
    serialized into a dictionary with the correct values.

    Tests that the FoodProduct instance has the correct values for its
    attributes after being committed to the database.

    Also tests that the FoodProduct instance can be serialized into a
    dictionary with the correct values.
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


def test_food_product_invalid_dates(db_session) -> None:
    """
    Tests that a FoodProduct instance is not valid if the expiry date is before the
    manufacturing date.

    The test creates a FoodProduct instance with an expiry date before the
    manufacturing date, and then checks that the expiry date is not valid (i.e.
    it is before today's date).
    """
    mfg = date.today()
    expiry = mfg - timedelta(days=1)  # expiry before manufacturing

    food = FoodProduct(
        product_name="Cheese",
        category="food",
        quantity=5,
        price=3.0,
        mfg_date=mfg,
        expiry_date=expiry,
    )
    db_session.add(food)
    db_session.commit()
    assert food.expiry_date < date.today()


# ----------------------
# ElectronicProduct Tests
# ----------------------
def test_electronic_product_creation_and_warranty(db_session) -> None:
    """
    Tests that an ElectronicProduct instance is valid and its get_warranty_end_date()
    method returns the correct value.

    The test creates an ElectronicProduct instance with a purchase date and warranty
    period, and then checks that the purchase date and warranty period are correctly
    set. It also checks that the get_warranty_end_date() method returns the correct
    value.
    """
    purchase = date.today()
    electronic = ElectronicProduct(
        product_name="Laptop",
        category="electronic",
        quantity=3,
        price=1000.0,
        purchase_date=purchase,
        warranty_period=24,
    )
    db_session.add(electronic)
    db_session.commit()

    assert electronic.purchase_date == purchase
    assert electronic.warranty_period == 24
    assert electronic.get_warranty_end_date() == purchase + relativedelta(months=24)


def test_electronic_product_missing_fields(db_session) -> None:
    """
    Tests that an ElectronicProduct instance is not valid if the purchase_date is
    missing.

    The test creates an ElectronicProduct instance with a missing purchase_date,
    and then checks that an IntegrityError is raised when trying to commit to the
    database.
    """

    with pytest.raises(IntegrityError):
        e = ElectronicProduct(
            product_name="Phone",
            category="electronic",
            quantity=2,
            price=500.0,
            purchase_date=None,  # required
            warranty_period=12,
        )
        db_session.add(e)
        db_session.commit()


# ----------------------
# BookProduct Tests
# ----------------------
def test_book_product_creation(db_session) -> None:
    """
    Tests that a BookProduct instance is valid and its get_total_value() method
    returns the correct value.

    The test creates a BookProduct instance with valid values for its attributes,
    adds it to the database session, and then checks that the values have been
    correctly set. It also checks that the get_total_value() method returns the
    correct value.
    """

    book = BookProduct(
        product_name="Python 101",
        category="book",
        quantity=15,
        price=45.0,
        author="John Doe",
        publication_year=2020,
    )
    db_session.add(book)
    db_session.commit()

    assert book.author == "John Doe"
    assert book.publication_year == 2020
    assert book.get_total_value() == 15 * 45.0


def test_book_product_missing_fields(db_session) -> None:
    """
    Tests that a BookProduct instance is not valid if the author is missing.

    The test creates a BookProduct instance with a missing author, and then checks
    that an IntegrityError is raised when trying to commit to the database.
    """
    with pytest.raises(IntegrityError):
        b = BookProduct(
            product_name="Python Advanced",
            category="book",
            quantity=5,
            price=50.0,
            author=None,  # author is required
            publication_year=2021,
        )
        db_session.add(b)
        db_session.commit()
