from typing import Dict, Generator

import pytest
from api.routes.inventory import inventory, inventory_bp
from flask import Flask


# ---------- Fixtures ----------
@pytest.fixture(autouse=True)
def clear_inventory() -> Generator[None, None, None]:
    """
    Clear the in-memory inventory before and after each test to avoid test pollution.
    """
    inventory.products.clear()
    yield
    inventory.products.clear()


@pytest.fixture
def client() -> Generator:
    """
    Return a Flask test client with the inventory blueprint registered.

    Yields:
        FlaskClient: The test client for sending HTTP requests.
    """
    app = Flask(__name__)
    app.register_blueprint(inventory_bp, url_prefix="/api")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------- Sample product data ----------
@pytest.fixture
def base_product() -> Dict:
    """Return a base product dictionary."""
    return {
        "product_id": 1,
        "product_name": "Test Product",
        "quantity": 5,
        "price": 10.0,
        "category": "Test",
        "mfg_date": "2025-01-01",
        "expiry_date": "2026-01-01",
        "purchase_date": "2025-08-14",
    }


@pytest.fixture
def second_product() -> Dict:
    """Return a second sample product dictionary."""
    return {
        "product_id": 2,
        "product_name": "Second Product",
        "quantity": 3,
        "price": 15.0,
        "category": "Test",
        "mfg_date": "2025-02-01",
        "expiry_date": "2026-02-01",
        "purchase_date": "2025-08-15",
    }
