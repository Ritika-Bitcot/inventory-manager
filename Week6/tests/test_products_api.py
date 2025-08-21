from datetime import date
from typing import Any
from unittest.mock import patch

from api.models import FoodProduct
from flask_sqlalchemy.session import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.scoping import scoped_session

# from Week6.api.routes.products import delete_product


# ----------------------
# GET /api/products/
# ----------------------
def test_get_products_success(client: Any, db_session: scoped_session[Session]):
    product = FoodProduct(
        product_name="burger",
        category="food",
        quantity=10,
        price=3.5,
        mfg_date=date(2025, 8, 1),
        expiry_date=date(2025, 8, 30),
    )
    db_session.add(product)
    db_session.commit()

    resp = client.get("/api/products/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "products" in data
    assert any(p["product_name"] == "burger" for p in data["products"])


def test_get_products_db_error(client: Any):
    with patch("api.routes.products.Product.query") as mock_query:
        mock_query.all.side_effect = SQLAlchemyError("DB fail")
        resp = client.get("/api/products/")
        assert resp.status_code == 500
        assert resp.get_json()["error"] == "Database error"


# ----------------------
# GET /api/products/<id>
# ----------------------
def test_get_product_success(client: Any, db_session: scoped_session[Session]):
    product = FoodProduct(
        product_name="Banana",
        category="food",
        price=5.0,
        quantity=15,
        mfg_date=date(2025, 11, 15),
        expiry_date=date(2025, 11, 22),
    )
    db_session.add(product)
    db_session.commit()

    resp = client.get(f"/api/products/{product.id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["product_name"] == "Banana"


def test_get_product_not_found(client: Any):
    resp = client.get("/api/products/999")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


def test_get_product_db_error(client: Any):
    with patch("api.routes.products.Product.query") as mock_query:
        mock_query.get.side_effect = SQLAlchemyError("DB fail")

        resp = client.get("/api/products/1")
        assert resp.status_code == 500
        assert resp.get_json()["error"] == "Database error"


# ----------------------
# POST /api/products/
# ----------------------
def test_create_product_success(client: Any):
    payload = {
        "product_name": "Cake",
        "category": "food",
        "price": 350.0,
        "quantity": 3,
        "mfg_date": "2025-09-21",
        "expiry_date": "2025-11-21",
    }
    resp = client.post("/api/products/", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["message"] == "Product created"
    assert data["product"]["product_name"] == "Cake"


def test_create_product_invalid_category(client: Any):
    resp = client.post("/api/products/", json={"name": "X", "category": "invalid"})
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Invalid category"


def test_create_product_validation_error(client: Any):
    resp = client.post("/api/products/", json={"category": "food"})  # missing fields
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"


def test_create_product_integrity_error(client: Any):
    payload = {
        "product_name": "Yogurt",
        "category": "food",
        "price": 50.0,
        "quantity": 30,
        "mfg_date": "2025-11-01",
        "expiry_date": "2026-01-01",
    }
    with patch(
        "api.routes.products.db.session.commit",
        side_effect=IntegrityError("mock", "mock", "mock"),
    ):
        resp = client.post("/api/products/", json=payload)
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Integrity error"


def test_create_product_db_error(client: Any):
    payload = {
        "product_name": "French Fries",
        "category": "food",
        "price": 159.0,
        "quantity": 10,
        "mfg_date": "2025-06-07",
        "expiry_date": "2025-06-21",
    }
    with patch(
        "api.routes.products.db.session.commit",
        side_effect=SQLAlchemyError("mock db error"),
    ):
        resp = client.post("/api/products/", json=payload)
    assert resp.status_code == 500
    assert resp.get_json()["error"] == "Database error"


# ----------------------
# PUT /api/products/<id>
# ----------------------


def test_update_product_not_found(client: Any):
    resp = client.put("/api/products/999", json={"price": 100})
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


def test_update_product_success(client: Any, db_session: scoped_session[Session]):
    product = FoodProduct(
        product_name="Rice",
        category="food",
        quantity=50,
        price=20.0,
        mfg_date=date(2025, 7, 1),
        expiry_date=date(2025, 12, 31),
    )
    db_session.add(product)
    db_session.commit()

    resp = client.put(f"/api/products/{product.id}", json={"price": 25, "quantity": 40})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "Product updated"
    assert data["product"]["price"] == 25


def test_update_product_validation_error(
    client: Any, db_session: scoped_session[Session]
):
    product = FoodProduct(
        product_name="Bread",
        category="food",
        quantity=30,
        price=2.0,
        mfg_date=date(2025, 8, 1),
        expiry_date=date(2025, 8, 10),
    )
    db_session.add(product)
    db_session.commit()

    resp = client.put(f"/api/products/{product.id}", json={"price": "invalid"})
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"


def test_update_product_integrity_error(
    client: Any, db_session: scoped_session[Session]
):
    product = FoodProduct(
        product_name="Cake",
        category="food",
        quantity=5,
        price=15.0,
        mfg_date=date(2025, 7, 15),
        expiry_date=date(2025, 7, 20),
    )
    db_session.add(product)
    db_session.commit()

    with patch(
        "api.routes.products.db.session.commit",
        side_effect=IntegrityError("mock", "mock", "mock"),
    ):
        resp = client.put(f"/api/products/{product.id}", json={"price": 20})

    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Integrity error"


def test_update_product_db_error(client: Any, db_session: scoped_session[Session]):
    product = FoodProduct(
        product_name="Fish",
        category="food",
        quantity=2,
        price=50.0,
        mfg_date=date(2025, 8, 1),
        expiry_date=date(2025, 8, 5),
    )
    db_session.add(product)
    db_session.commit()

    with patch(
        "api.routes.products.db.session.commit",
        side_effect=SQLAlchemyError("mock db error"),
    ):
        resp = client.put(f"/api/products/{product.id}", json={"price": 60})

    assert resp.status_code == 500
    assert resp.get_json()["error"] == "Database error"


# ----------------------
# DELETE /api/products/<id>
# ----------------------
def test_delete_product_success(client: Any, db_session: scoped_session[Session]):
    product = FoodProduct(
        product_name="Juice",
        category="food",
        quantity=12,
        price=8.0,
        mfg_date=date(2025, 8, 1),
        expiry_date=date(2025, 8, 10),
    )
    db_session.add(product)
    db_session.commit()

    resp = client.delete(f"/api/products/{product.id}")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Product deleted"


def test_delete_product_db_error(client: Any, db_session: scoped_session[Session]):
    product = FoodProduct(
        product_name="Soap",
        category="food",
        quantity=3,
        price=2.0,
        mfg_date=date(2025, 8, 1),
        expiry_date=date(2025, 8, 5),
    )
    db_session.add(product)
    db_session.commit()

    with patch(
        "api.routes.products.db.session.commit",
        side_effect=SQLAlchemyError("mock delete error"),
    ):
        resp = client.delete(f"/api/products/{product.id}")

    assert resp.status_code == 500
    assert resp.get_json()["error"] == "Database error"


# def test_delete_product_not_found(app_context):
#     with patch.object(Product.query, "get", return_value=None):
#         response, status_code = delete_product(product_id=123)

#     assert status_code == 404
#     assert response.get_json() == {"error": "Product not found"}
