from datetime import date
from typing import Dict
from unittest.mock import patch

from api.models import FoodProduct
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


# ----------------------
# Protected Route Tests
# ----------------------
def test_protected_route_without_token(client) -> None:
    """Accessing protected route without token should return 401."""
    resp = client.get("/api/products/")
    data = resp.get_json()
    assert resp.status_code == 401
    assert any(k in data for k in ("msg", "error"))


def test_staff_user_cannot_create_product(
    client, staff_auth_header: Dict[str, str]
) -> None:
    """Staff users cannot create products."""
    resp = client.post(
        "/api/products/",
        headers=staff_auth_header,
        json={"product_name": "Test Product", "price": 10.0},
    )
    assert resp.status_code == 403
    data = resp.get_json()
    assert any(k in data for k in ("msg", "error"))


def test_admin_can_delete_product(client, admin_auth_header: Dict[str, str]) -> None:
    """Admin users can delete a product successfully."""
    payload = {
        "product_name": "DeleteMe",
        "category": "food",
        "quantity": 5,
        "price": 10.0,
        "mfg_date": "2025-09-01",
        "expiry_date": "2026-09-01",
    }
    create_resp = client.post("/api/products/", headers=admin_auth_header, json=payload)
    product_id = create_resp.get_json()["product"]["id"]

    delete_resp = client.delete(
        f"/api/products/{product_id}", headers=admin_auth_header
    )
    assert delete_resp.status_code == 200
    assert delete_resp.get_json()["message"] == "Product deleted"


# ----------------------
# Forbidden/Delete Tests
# ----------------------
def test_delete_product_forbidden(
    client, db_session: Session, staff_auth_header, test_user
) -> None:
    """Staff users should not delete products."""
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
    assert "error" in resp.get_json() or "msg" in resp.get_json()


def test_delete_product_invalid_id(client, admin_auth_header: Dict[str, str]) -> None:
    """Deleting a product with invalid ID returns 404 or 400."""
    resp = client.delete("/api/products/invalid", headers=admin_auth_header)
    assert resp.status_code in (404, 400)


def test_delete_product_database_error(
    client, admin_auth_header, db_session: Session, test_user
) -> None:
    """Simulate database error when deleting a product."""
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

    with patch(
        "api.db.db.session.commit", side_effect=SQLAlchemyError("Forced DB error")
    ):
        resp = client.delete(f"/api/products/{product.id}", headers=admin_auth_header)
        data = resp.get_json()
        assert resp.status_code == 500
        assert data["error"] == "Database error"
        assert "Forced DB error" in data["details"]
