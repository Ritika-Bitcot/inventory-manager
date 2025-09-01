from datetime import date
from typing import Dict
from unittest.mock import patch

from api.models import FoodProduct
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


# ----------------------
# Helper functions
# ----------------------
def create_food_product(
    db_session: Session,
    name: str,
    owner_id: str,
    quantity: int = 10,
    price: float = 10.0,
    mfg_date: date = date(2025, 1, 1),
    expiry_date: date = date(2025, 12, 31),
) -> FoodProduct:
    """Utility to create a FoodProduct in the database."""
    product = FoodProduct(
        product_name=name,
        category="food",
        quantity=quantity,
        price=price,
        mfg_date=mfg_date,
        expiry_date=expiry_date,
        owner_id=owner_id,
    )
    db_session.add(product)
    db_session.commit()
    return product


# ----------------------
# GET /api/products/
# ----------------------
def test_get_products_non_empty(client, auth_header: Dict[str, str]) -> None:
    """Ensure GET /api/products/ returns a non-empty list when products exist."""
    resp = client.get("/api/products/", headers=auth_header)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "products" in data
    assert len(data["products"]) > 0
    assert any(p["product_name"] == "Generic" for p in data["products"])


def test_get_products_list(
    client, db_session: Session, auth_header: Dict[str, str], test_user
) -> None:
    """GET /api/products/ returns the product created in DB."""
    _ = create_food_product(db_session, "Phone", str(test_user.id))
    resp = client.get("/api/products/", headers=auth_header)
    assert resp.status_code == 200
    data = resp.get_json()["products"]
    assert any(p["product_name"] == "Phone" for p in data)


def test_get_products_database_error(client, auth_header: Dict[str, str]) -> None:
    """Simulate database error during GET /api/products/"""
    with patch("api.models.Product.query") as mock_query:
        mock_query.all.side_effect = SQLAlchemyError("Forced DB error")
        resp = client.get("/api/products/", headers=auth_header)
        data = resp.get_json()
        assert resp.status_code == 500
        assert data["error"] == "Database error"
        assert "Forced DB error" in data["details"]


# ----------------------
# GET /api/products/<id>
# ----------------------
def test_get_product_database_error(client, auth_header: Dict[str, str]) -> None:
    """Simulate database error during GET /api/products/<id>"""
    with patch("api.models.Product.query") as mock_query:
        mock_query.get.side_effect = SQLAlchemyError("Forced DB error")
        resp = client.get("/api/products/1", headers=auth_header)
        data = resp.get_json()
        assert resp.status_code == 500
        assert data["error"] == "Database error"
        assert "Forced DB error" in data["details"]


# ----------------------
# POST /api/products/
# ----------------------
def test_create_product_success(client, auth_header: Dict[str, str]) -> None:
    """Successful product creation."""
    payload = {
        "product_name": "Cake",
        "category": "food",
        "price": 50.0,
        "quantity": 3,
        "mfg_date": "2025-09-21",
        "expiry_date": "2025-11-21",
    }
    resp = client.post("/api/products/", json=payload, headers=auth_header)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["message"] == "Product created"
    assert data["product"]["product_name"] == "Cake"


def test_create_product_validation_error(client, auth_header: Dict[str, str]) -> None:
    """Creating product with missing fields returns 400."""
    resp = client.post("/api/products/", json={"category": "food"}, headers=auth_header)
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"


def test_create_product_invalid_category(client, auth_header: Dict[str, str]) -> None:
    """Creating product with invalid category returns 400."""
    resp = client.post(
        "/api/products/",
        json={"product_name": "X", "category": "invalid"},
        headers=auth_header,
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Invalid category"


def test_create_product_integrity_error(client, auth_header: Dict[str, str]) -> None:
    """Simulate IntegrityError during product creation."""
    payload = {
        "product_name": "Cake",
        "category": "food",
        "price": 50.0,
        "quantity": 3,
        "mfg_date": "2025-09-21",
        "expiry_date": "2025-11-21",
    }
    with patch(
        "api.db.db.session.commit",
        side_effect=IntegrityError("Forced Integrity", "params", "orig"),
    ):
        resp = client.post("/api/products/", json=payload, headers=auth_header)
        data = resp.get_json()
        assert resp.status_code == 400
        assert data["error"] == "Integrity error"
        assert "Forced Integrity" in data["details"]


def test_create_product_database_error(client, auth_header: Dict[str, str]) -> None:
    """Simulate SQLAlchemyError during product creation."""
    payload = {
        "product_name": "Cake",
        "category": "food",
        "price": 50.0,
        "quantity": 3,
        "mfg_date": "2025-09-21",
        "expiry_date": "2025-11-21",
    }
    with patch(
        "api.db.db.session.commit", side_effect=SQLAlchemyError("Forced DB error")
    ):
        resp = client.post("/api/products/", json=payload, headers=auth_header)
        data = resp.get_json()
        assert resp.status_code == 500
        assert data["error"] == "Database error"
        assert "Forced DB error" in data["details"]


# ----------------------
# PUT /api/products/<id>
# ----------------------
def test_update_product_success(
    client, db_session: Session, auth_header: Dict[str, str], test_user
) -> None:
    """Successfully update product price and quantity."""
    product = create_food_product(db_session, "Rice", str(test_user.id))
    resp = client.put(
        f"/api/products/{product.id}",
        json={"price": 25, "quantity": 15},
        headers=auth_header,
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "Product updated"
    assert data["product"]["price"] == 25


def test_update_product_not_found(client, auth_header: Dict[str, str]) -> None:
    """Updating a non-existent product returns 404."""
    resp = client.put("/api/products/999", json={"price": 99}, headers=auth_header)
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


def test_update_product_invalid_data(
    client, db_session: Session, auth_header: Dict[str, str], test_user
) -> None:
    """Sending invalid data should return 400."""
    product = create_food_product(db_session, "RiceInvalid", str(test_user.id))
    resp = client.put(
        f"/api/products/{product.id}",
        json={"quantity": "invalid"},  # invalid type
        headers=auth_header,
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_update_product_integrity_error(
    client, admin_auth_header: Dict[str, str], test_user, db_session: Session
) -> None:
    """Simulate IntegrityError during product update."""
    product = create_food_product(db_session, "IntegrityTest", str(test_user.id))
    with patch(
        "api.db.db.session.commit",
        side_effect=IntegrityError("Forced Integrity", "params", "orig"),
    ):
        resp = client.put(
            f"/api/products/{product.id}",
            json={"price": 20.0},
            headers=admin_auth_header,
        )
        data = resp.get_json()
        assert resp.status_code == 400
        assert data["error"] == "Integrity error"
        assert "Forced Integrity" in data["details"]


def test_update_product_database_error(
    client, admin_auth_header: Dict[str, str], test_user, db_session: Session
) -> None:
    """Simulate SQLAlchemyError during product update."""
    product = create_food_product(db_session, "DBErrorUpdate", str(test_user.id))
    with patch(
        "api.db.db.session.commit", side_effect=SQLAlchemyError("Forced DB error")
    ):
        resp = client.put(
            f"/api/products/{product.id}",
            json={"price": 20.0},
            headers=admin_auth_header,
        )
        data = resp.get_json()
        assert resp.status_code == 500
        assert data["error"] == "Database error"
        assert "Forced DB error" in data["details"]


# ----------------------
# DELETE /api/products/<id>
# ----------------------
def test_delete_product_success(
    client, db_session: Session, auth_header: Dict[str, str], test_user
) -> None:
    """Successfully delete a product."""
    product = create_food_product(db_session, "Juice", str(test_user.id))
    resp = client.delete(f"/api/products/{product.id}", headers=auth_header)
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Product deleted"

    resp = client.get("/api/products/", headers=auth_header)
    assert all(p["id"] != product.id for p in resp.get_json()["products"])


def test_delete_product_not_found(client, auth_header: Dict[str, str]) -> None:
    """Deleting a non-existent product returns 404."""
    resp = client.delete("/api/products/999", headers=auth_header)
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


def test_delete_product_database_error(
    client, admin_auth_header: Dict[str, str], db_session: Session, test_user
) -> None:
    """Simulate SQLAlchemyError during DELETE /api/products/<id>"""
    product = create_food_product(db_session, "DBErrorDelete", str(test_user.id))
    with patch(
        "api.db.db.session.commit", side_effect=SQLAlchemyError("Forced DB error")
    ):
        resp = client.delete(f"/api/products/{product.id}", headers=admin_auth_header)
        data = resp.get_json()
        assert resp.status_code == 500
        assert data["error"] == "Database error"
        assert "Forced DB error" in data["details"]


# ----------------------
# GET /api/products/ with owner
# ----------------------
def test_get_products_with_owner(
    client, db_session: Session, test_user, auth_header: Dict[str, str]
) -> None:
    """Ensure products with a valid owner serialize correctly."""
    _ = create_food_product(db_session, "OrphanFixed", str(test_user.id))
    resp = client.get("/api/products/", headers=auth_header)
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(p["product_name"] == "OrphanFixed" for p in data["products"])


# ----------------------
# POST missing dates
# ----------------------
def test_create_product_missing_dates(client, auth_header: Dict[str, str]) -> None:
    """Creating food product without mfg/expiry dates should fail."""
    resp = client.post(
        "/api/products/",
        headers=auth_header,
        json={"product_name": "Cake2", "category": "food", "price": 10, "quantity": 1},
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()
