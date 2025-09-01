from datetime import date
from unittest.mock import patch

from api.models import FoodProduct
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


# ----------------------
# GET /api/products/
# ----------------------
def test_get_products_non_empty(client, auth_header):
    resp = client.get("/api/products/", headers=auth_header)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "products" in data
    assert len(data["products"]) > 0  # Products should exist
    # optionally check one field from seeded data
    assert any(p["product_name"] == "Generic" for p in data["products"])


def test_get_products_list(client, db_session: Session, auth_header, test_user):
    product = FoodProduct(
        product_name="Phone",
        category="food",
        quantity=10,
        price=100.0,
        mfg_date=date(2025, 1, 1),
        expiry_date=date(2025, 12, 31),
        owner_id=str(test_user.id),  # real user UUID
    )
    db_session.add(product)
    db_session.commit()

    resp = client.get("/api/products/", headers=auth_header)
    assert resp.status_code == 200
    data = resp.get_json()["products"]
    assert any(p["product_name"] == "Phone" for p in data)


# ----------------------
# POST /api/products/
# ----------------------
def test_create_product_success(client, auth_header):
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


def test_create_product_validation_error(client, auth_header):
    # Missing required fields
    resp = client.post("/api/products/", json={"category": "food"}, headers=auth_header)
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"


def test_create_product_invalid_category(client, auth_header):
    resp = client.post(
        "/api/products/",
        json={"product_name": "X", "category": "invalid"},
        headers=auth_header,
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Invalid category"


# ----------------------
# PUT /api/products/<id>
# ----------------------
def test_update_product_success(client, db_session: Session, auth_header, test_user):
    product = FoodProduct(
        product_name="Rice",
        category="food",
        quantity=10,
        price=20.0,
        mfg_date=date(2025, 7, 1),
        expiry_date=date(2025, 12, 31),
        owner_id=str(test_user.id),
    )
    db_session.add(product)
    db_session.commit()

    resp = client.put(
        f"/api/products/{product.id}",
        json={"price": 25, "quantity": 15},
        headers=auth_header,
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "Product updated"
    assert data["product"]["price"] == 25


def test_update_product_not_found(client, auth_header):
    resp = client.put("/api/products/999", json={"price": 99}, headers=auth_header)
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


# ----------------------
# DELETE /api/products/<id>
# ----------------------
def test_delete_product_success(client, db_session: Session, auth_header, test_user):
    product = FoodProduct(
        product_name="Juice",
        category="food",
        quantity=5,
        price=10.0,
        mfg_date=date(2025, 8, 1),
        expiry_date=date(2025, 8, 10),
        owner_id=str(test_user.id),
    )
    db_session.add(product)
    db_session.commit()

    resp = client.delete(f"/api/products/{product.id}", headers=auth_header)
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Product deleted"

    resp = client.get("/api/products/", headers=auth_header)
    assert all(p["id"] != product.id for p in resp.get_json()["products"])


def test_delete_product_not_found(client, auth_header):
    resp = client.delete("/api/products/999", headers=auth_header)
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


# ----------------------
# GET /api/products/ with owner
# ----------------------
def test_get_products_with_owner(client, db_session: Session, test_user, auth_header):
    """Ensure products with a valid owner serialize correctly."""
    product = FoodProduct(
        product_name="OrphanFixed",
        category="food",
        quantity=1,
        price=1.0,
        mfg_date=date(2025, 1, 1),
        expiry_date=date(2025, 12, 31),
        owner_id=str(test_user.id),  # assign owner
    )
    db_session.add(product)
    db_session.commit()

    resp = client.get("/api/products/", headers=auth_header)
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(p["product_name"] == "OrphanFixed" for p in data["products"])


# ----------------------
# PUT /api/products/<id> invalid data
# ----------------------
def test_update_product_invalid_data(
    client, db_session: Session, auth_header, test_user
):
    """Sending invalid data should return 400."""
    product = FoodProduct(
        product_name="RiceInvalid",
        category="food",
        quantity=10,
        price=20.0,
        mfg_date=date(2025, 7, 1),
        expiry_date=date(2025, 12, 31),
        owner_id=str(test_user.id),
    )
    db_session.add(product)
    db_session.commit()

    resp = client.put(
        f"/api/products/{product.id}",
        json={"quantity": "invalid"},  # invalid type
        headers=auth_header,
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


# ----------------------
# POST /api/products/ missing fields
# ----------------------
def test_create_product_missing_dates(client, auth_header):
    """Creating food product without mfg/expiry dates should fail."""
    resp = client.post(
        "/api/products/",
        headers=auth_header,
        json={"product_name": "Cake2", "category": "food", "price": 10, "quantity": 1},
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_update_product_integrity_error(
    client, admin_auth_header, test_user, db_session
):
    """Simulate IntegrityError during product update."""
    # Create a product
    product = FoodProduct(
        product_name="IntegrityTest",
        category="food",
        quantity=5,
        price=10.0,
        mfg_date="2025-08-01",
        expiry_date="2025-08-10",
        owner_id=str(test_user.id),
    )
    db_session.add(product)
    db_session.commit()

    update_payload = {"price": 20.0}

    # Mock db.session.commit to raise IntegrityError
    with patch(
        "api.db.db.session.commit",
        side_effect=IntegrityError("Forced Integrity", "params", "orig"),
    ):
        resp = client.put(
            f"/api/products/{product.id}",
            json=update_payload,
            headers=admin_auth_header,
        )
        data = resp.get_json()
        assert resp.status_code == 400
        assert data["error"] == "Integrity error"
        assert "Forced Integrity" in data["details"]
