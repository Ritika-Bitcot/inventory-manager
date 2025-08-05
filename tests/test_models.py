from datetime import datetime, timedelta

import pydantic
import pytest
from pydantic import ValidationError

from Week3.models import (
    PRODUCT_CLASS_MAP,
    BookProduct,
    ElectronicProduct,
    FoodProduct,
    Product,
)


@pytest.mark.parametrize(
    "quantity, price, expected",
    [
        (10, 5.0, 50.0),
        (0, 100.0, 0.0),
        (3, 33.33, 99.99),
        (1000_000, 1000.0, 1_000_000_000.0),
        (0, 0.01, 0.0),
    ],
)
def test_get_total_value(quantity, price, expected) -> None:
    """
    Tests the get_total_value method of the Product class.

    The test uses a parametrize decorator to run the test
    function multiple times with different inputs.
    """
    product = Product(
        product_id=1,
        product_name="Sample",
        category="Test",
        quantity=quantity,
        price=price,
    )
    assert product.get_total_value() == pytest.approx(expected, 0.01)


def test_product_should_raise_validation_error_on_negative_price() -> None:
    """
    Tests that creating a Product with a negative price raises a ValidationError.

    This test ensures that the Product model enforces the constraint that
    the price must be greater than zero, as defined in the Product class
    using Pydantic's Field validation.
    """

    with pytest.raises(ValidationError):
        Product(
            product_id=1,
            product_name="Sample",
            category="Test",
            quantity=10,
            price=-1.0,
        )


def test_product_invalid_data_types():
    """Should raise ValidationError for incorrect types (e.g., price=str)"""
    with pytest.raises(pydantic.ValidationError):
        Product(
            product_id="abc",  # str instead of int
            product_name="Test Product",
            quantity="ten",  # str instead of int
            price="100.50",  # str instead of float
        )


@pytest.mark.parametrize(
    "field, value",
    [
        ("product_id", 0),
        ("product_name", "ab"),
        ("quantity", -1),
        ("price", -10),
    ],
)
def test_product_invalid_fields(field, value) -> None:
    """Should raise ValueError for invalid field constraints"""
    kwargs = {
        "product_id": 1,
        "product_name": "Valid Name",
        "quantity": 10,
        "price": 100.0,
    }
    kwargs[field] = value
    with pytest.raises(ValueError):
        Product(**kwargs)


def test_product_price_just_above_zero() -> None:
    """Should allow price slightly above 0"""
    product = Product(product_id=1, product_name="Pen", quantity=1, price=0.0001)
    assert product.price > 0


def test_product_name_unicode() -> None:
    """Should accept Unicode/special characters in name"""
    product = Product(product_id=5, product_name="Café ☕", quantity=2, price=10)
    assert "Café" in product.product_name


def test_product_with_missing_optional_category() -> None:
    product = Product(product_id=10, product_name="No Category", quantity=5, price=10)
    assert product.category is None


# FoodProduct Tests


def test_food_product_valid_dates() -> None:
    """
    Tests that food products have valid dates
    """
    today = datetime.today()
    food = FoodProduct(
        product_id=1,
        product_name="Milk",
        quantity=5,
        price=20,
        mfg_date=today,
        expiry_date=today + timedelta(days=10),
    )

    assert food.expiry_date > food.mfg_date


def test_food_product_invalid_expiry() -> None:
    """
    Tests that creating a FoodProduct with an expiry date
    before the manufacturing date raises a ValueError
    with a message indicating that `the expiry date must
    be after the manufacturing date`.
    """
    today = datetime.today()
    with pytest.raises(ValueError, match="expiry_date must be after mfg_date"):
        FoodProduct(
            product_id=2,
            product_name="Expired",
            quantity=5,
            price=20,
            mfg_date=today,
            expiry_date=today - timedelta(days=1),
        )


def test_electronic_product_warranty() -> None:
    """
    Tests that the get_warranty_end_date method of the
    ElectronicProduct class returns the correct end date
    based on the purchase date and warranty period.
    """
    purchase_date = datetime(2024, 1, 1)
    product = ElectronicProduct(
        product_id=3,
        product_name="Phone",
        quantity=1,
        price=999,
        purchase_date=purchase_date,
        warranty_period=12,
    )
    expected_end_date = datetime(2025, 1, 1)
    assert product.get_warranty_end_date() == expected_end_date


def test_electronic_product_negative_warranty() -> None:
    """
    Tests that creating an ElectronicProduct
    with a negative warranty period raises a ValueError.
    """
    with pytest.raises(ValueError):
        ElectronicProduct(
            product_id=4,
            product_name="TV",
            quantity=1,
            price=150000,
            purchase_date=datetime.now(),
            warranty_period=-1,
        )


def test_product_name_max_length() -> None:
    name = "x" * 50
    product = Product(product_id=1, product_name=name, quantity=1, price=10)
    assert product.product_name == name


def test_electronic_product_zero_warranty() -> None:
    """Warranty end date should equal purchase date for 0-month warranty"""
    date = datetime(2023, 1, 1)
    product = ElectronicProduct(
        product_id=42,
        product_name="USB Drive",
        quantity=1,
        price=500,
        purchase_date=date,
        warranty_period=0,
    )
    assert product.get_warranty_end_date() == date


# BookProduct Tests


def test_book_product_valid() -> None:
    """
    Tests that a valid BookProduct is created
    with the correct author and publication year.

    """

    book = BookProduct(
        product_id=5,
        product_name="Python 101",
        quantity=3,
        price=500,
        author="John Doe",
        publication_year=2023,
    )
    assert book.author == "John Doe"
    assert book.publication_year == 2023


def test_book_product_invalid_author() -> None:
    """
    Tests that creating a BookProduct
    with an invalid author raises a ValueError.
    """
    with pytest.raises(ValueError):
        BookProduct(
            product_id=6,
            product_name="Invalid Book",
            quantity=1,
            price=300,
            author="JD",
            publication_year=2022,
        )


def test_book_product_future_year() -> None:
    """
    Tests that a BookProduct raises a ValueError
    when created with a future year
    (a year greater than the current year).
    """
    with pytest.raises(ValueError):
        BookProduct(
            product_id=7,
            product_name="Time Travel",
            quantity=1,
            price=300,
            author="Author X",
            publication_year=datetime.now().year + 1,  # future year
        )


# Unkown Product Type
def test_unregistered_product_category_returns_none() -> None:
    """
    Tests that attempting to get a product class from the
    PRODUCT_CLASS_MAP registry with an unregistered category
    returns None.
    """
    assert PRODUCT_CLASS_MAP.get("furniture") is None
