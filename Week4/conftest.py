# tests/conftest.py

from datetime import datetime, timedelta

import pytest

from Week3.core import Inventory
from Week3.models import BookProduct, ElectronicProduct, FoodProduct, Product

# ----------------------------
# Product Fixtures
# ----------------------------


@pytest.fixture
def sample_product() -> Product:
    """
    Provides a generic Product instance for testing.

    Returns:
        Product: ID 1, name "Pen", category "stationery",
        quantity 10, price 5.0.
    """
    return Product(
        product_id=1,
        product_name="Pen",
        category="stationery",
        quantity=10,
        price=5.0,
    )


@pytest.fixture
def food_product() -> FoodProduct:
    """
    Provides a FoodProduct instance for testing.

    Returns:
        FoodProduct: ID 2, name "Milk", quantity 5, price 20.0,
        manufacturing date 2 days ago, expiry date 5 days from now.
    """
    today = datetime.now()
    return FoodProduct(
        product_id=2,
        product_name="Milk",
        quantity=5,
        price=20.0,
        mfg_date=today - timedelta(days=2),
        expiry_date=today + timedelta(days=5),
    )


@pytest.fixture
def electronic_product() -> ElectronicProduct:
    """
    Provides an ElectronicProduct instance for testing.

    Returns:
        ElectronicProduct: ID 3, name "Phone", quantity 2, price 1000.0,
        purchase date 2024-01-01, warranty period 12 months.
    """
    return ElectronicProduct(
        product_id=3,
        product_name="Phone",
        quantity=2,
        price=1000.0,
        purchase_date=datetime(2024, 1, 1),
        warranty_period=12,
    )


@pytest.fixture
def book_product() -> BookProduct:
    """
    Provides a BookProduct instance for testing.

    Returns:
        BookProduct: ID 4, name "Clean Code", quantity 7, price 800.0,
        author "Robert Martin", publication year 2020.
    """
    return BookProduct(
        product_id=4,
        product_name="Clean Code",
        quantity=7,
        price=800.0,
        author="Robert Martin",
        publication_year=2020,
    )


# ----------------------------
# Inventory Fixture
# ----------------------------


@pytest.fixture
def inventory_with_products(
    sample_product,
    food_product,
    electronic_product,
    book_product,
) -> Inventory:
    """
    Provides an Inventory instance populated with sample products.

    Includes:
    - Generic Product
    - FoodProduct (Milk)
    - ElectronicProduct (Phone)
    - BookProduct (Clean Code)

    Returns:
        Inventory: Instance containing the sample products.
    """
    inventory = Inventory()
    inventory.products.extend(
        [
            sample_product,
            food_product,
            electronic_product,
            book_product,
        ]
    )
    return inventory
