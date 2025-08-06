# tests/conftest.py

from datetime import datetime, timedelta

import pytest

from Week3.core import Inventory
from Week3.models import BookProduct, ElectronicProduct, FoodProduct, Product


@pytest.fixture
def sample_product() -> Product:
    """
    Fixture that provides a sample Product instance for testing purposes.

    Returns:
        Product: A Product instance with id 1, name "Pen", quantity 10, price 5.0,
            and category "stationery".
    """

    return Product(
        product_id=1, product_name="Pen", quantity=10, price=5.0, category="stationery"
    )


@pytest.fixture
def food_product() -> FoodProduct:
    """
    Fixture that provides a FoodProduct instance for testing purposes.

    Returns:
        FoodProduct: An instance with id 2, name "Milk", quantity 5, price 20.0,
            manufacturing date 2 days ago, and an expiry date 5 days from now.
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
    Fixture that provides an ElectronicProduct instance for testing purposes.

    Returns:
        ElectronicProduct: An instance with id 3, name "Phone", quantity 2, price 1000.0,
            purchase date of January 1, 2024, and a warranty period of 12 months.
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
    Fixture that provides a BookProduct instance for testing purposes.

    Returns:
        BookProduct: A BookProduct instance with id 4, name "Clean Code", quantity 7, price 800.0,
            author "Robert Martin", and publication year 2020.
    """
    return BookProduct(
        product_id=4,
        product_name="Clean Code",
        quantity=7,
        price=800.0,
        author="Robert Martin",
        publication_year=2020,
    )


@pytest.fixture
def inventory_with_products(
    sample_product, food_product, electronic_product, book_product
) -> Inventory:
    """
    Fixture that provides an Inventory instance populated with sample products:
    - A generic Product
    - A FoodProduct (Milk)
    - An ElectronicProduct (Phone)
    - A BookProduct (Clean Code)

    Returns:
        Inventory: An instance of Inventory containing the sample products.
    """

    inventory = Inventory()
    inventory.products.extend(
        [sample_product, food_product, electronic_product, book_product]
    )
    return inventory
