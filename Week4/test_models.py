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

# =========================================================
# Product Tests
# =========================================================


@pytest.mark.parametrize(
    "quantity, price, expected",
    [
        (10, 5.0, 50.0),
        (0, 100.0, 0.0),
        (3, 33.33, 99.99),
        (1_000_000, 1000.0, 1_000_000_000.0),
        (0, 0.01, 0.0),
    ],
)
def test_get_total_value(quantity, price, expected) -> None:
    """Ensure get_total_value returns correct result."""
    product = Product(
        product_id=1,
        product_name="Sample",
        category="Test",
        quantity=quantity,
        price=price,
    )
    assert product.get_total_value() == pytest.approx(expected, 0.01)


def test_product_should_raise_validation_error_on_negative_price() -> None:
    """Negative price should raise ValidationError."""
    with pytest.raises(ValidationError):
        Product(
            product_id=1,
            product_name="Sample",
            category="Test",
            quantity=10,
            price=-1.0,
        )


def test_product_invalid_data_types() -> None:
    """Invalid data types should raise ValidationError."""
    with pytest.raises(pydantic.ValidationError):
        Product(
            product_id="abc",  # str instead of int
            product_name="Test",
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
    """Invalid field constraints should raise ValueError."""
    kwargs = dict(product_id=1, product_name="Valid Name", quantity=10, price=100.0)
    kwargs[field] = value
    with pytest.raises(ValueError):
        Product(**kwargs)


def test_product_price_just_above_zero() -> None:
    """Allow price slightly above zero."""
    product = Product(product_id=1, product_name="Pen", quantity=1, price=0.0001)
    assert product.price > 0


def test_product_name_unicode() -> None:
    """Allow Unicode characters in product_name."""
    product = Product(product_id=5, product_name="Café ☕", quantity=2, price=10)
    assert "Café" in product.product_name


def test_product_with_missing_optional_category() -> None:
    """Category can be None if not provided."""
    product = Product(product_id=10, product_name="No Category", quantity=5, price=10)
    assert product.category is None


def test_product_name_max_length() -> None:
    """Allow max length name."""
    name = "x" * 50
    product = Product(product_id=1, product_name=name, quantity=1, price=10)
    assert product.product_name == name


# =========================================================
# FoodProduct Tests
# =========================================================


def test_food_product_valid_dates() -> None:
    """Expiry date must be after manufacturing date."""
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
    """Expiry date before manufacturing date should raise ValueError."""
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


# =========================================================
# ElectronicProduct Tests
# =========================================================


def test_electronic_product_warranty() -> None:
    """get_warranty_end_date should return purchase_date + warranty_period months."""
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
    """Negative warranty should raise ValueError."""
    with pytest.raises(ValueError):
        ElectronicProduct(
            product_id=4,
            product_name="TV",
            quantity=1,
            price=150000,
            purchase_date=datetime.now(),
            warranty_period=-1,
        )


def test_electronic_product_zero_warranty() -> None:
    """Warranty end date should equal purchase date for 0-month warranty."""
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


# =========================================================
# BookProduct Tests
# =========================================================


def test_book_product_valid() -> None:
    """Valid BookProduct should have correct author and year."""
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
    """Invalid author name should raise ValueError."""
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
    """Future publication year should raise ValueError."""
    with pytest.raises(ValueError):
        BookProduct(
            product_id=7,
            product_name="Time Travel",
            quantity=1,
            price=300,
            author="Author X",
            publication_year=datetime.now().year + 1,
        )


# =========================================================
# Miscellaneous Tests
# =========================================================


def test_unregistered_product_category_returns_none() -> None:
    """Unknown product category should return None in PRODUCT_CLASS_MAP."""
    assert PRODUCT_CLASS_MAP.get("furniture") is None
