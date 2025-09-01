from datetime import date
from unittest.mock import patch

from api.models import FoodProduct
from pytest import Session
from sqlalchemy.exc import SQLAlchemyError


def test_protected_route_without_token(client):
    """Accessing a protected route without token should return 401."""
    resp = client.get("/api/products/")
    data = resp.get_json()
    assert resp.status_code == 401
    # Accept either {"msg": "..."} or {"error": "..."}
    assert any(k in data for k in ("msg", "error")), f"Unexpected response: {data}"


def test_staff_user_cannot_create_product(client, staff_auth_header):
    """Staff users should not be allowed to create products."""
    resp = client.post(
        "/api/products/",
        headers=staff_auth_header,
        json={"product_name": "Test Product", "price": 10.0},
    )
    assert resp.status_code == 403
    data = resp.get_json()
    assert any(k in data for k in ("msg", "error")), f"Unexpected response: {data}"


def test_admin_can_delete_product(client, admin_auth_header):
    """Admin should be able to delete a product."""
    # Create product as admin
    create_resp = client.post(
        "/api/products/",
        headers=admin_auth_header,
        json={
            "product_name": "DeleteMe",
            "category": "food",
            "quantity": 5,
            "price": 10.0,
            "mfg_date": "2025-09-01",
            "expiry_date": "2026-09-01",
        },
    )
    assert create_resp.status_code == 201
    product_id = create_resp.get_json()["product"]["id"]

    # Delete the product
    delete_resp = client.delete(
        f"/api/products/{product_id}", headers=admin_auth_header
    )
    assert delete_resp.status_code == 200
    assert delete_resp.get_json()["message"] == "Product deleted"

    # Confirm deletion
    get_resp = client.get("/api/products/", headers=admin_auth_header)
    assert all(p["id"] != product_id for p in get_resp.get_json()["products"])


# ----------------------
# DELETE forbidden for staff
# ----------------------
def test_delete_product_forbidden(
    client, db_session: Session, staff_auth_header, test_user
):
    """Staff should not be allowed to delete products."""
    product = FoodProduct(
        product_name="ProtectedJuice",
        category="food",
        quantity=5,
        price=10.0,
        mfg_date=date(2025, 8, 1),
        expiry_date=date(2025, 8, 10),
        owner_id=str(test_user.id),
    )
    db_session.add(product)
    db_session.commit()

    resp = client.delete(f"/api/products/{product.id}", headers=staff_auth_header)
    assert resp.status_code == 403
    data = resp.get_json()
    assert "error" in data or "msg" in data


def test_delete_product_invalid_id(client, admin_auth_header):
    """Deleting non-integer or invalid id should return 404."""
    resp = client.delete("/api/products/invalid", headers=admin_auth_header)
    assert resp.status_code in (404, 400)


def test_delete_product_database_error(
    client, admin_auth_header, test_user, db_session
):
    """Simulate a database error when deleting a product."""
    from api.models import FoodProduct

    # Create a product normally
    product = FoodProduct(
        product_name="DBErrorTest",
        category="food",
        quantity=5,
        price=10.0,
        mfg_date="2025-08-01",
        expiry_date="2025-08-10",
        owner_id=str(test_user.id),
    )
    db_session.add(product)
    db_session.commit()

    # Mock db.session.commit to raise SQLAlchemyError
    with patch(
        "api.db.db.session.commit", side_effect=SQLAlchemyError("Forced DB error")
    ):
        resp = client.delete(f"/api/products/{product.id}", headers=admin_auth_header)
        data = resp.get_json()
        assert resp.status_code == 500
        assert data["error"] == "Database error"
        assert "Forced DB error" in data["details"]
