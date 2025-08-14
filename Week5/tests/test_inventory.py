from typing import Dict
from unittest.mock import patch


# ---------- Basic API Endpoint Tests ----------
def test_hello_endpoint(client) -> None:
    """Test GET /hello returns a greeting message."""
    resp = client.get("/api/hello")
    assert resp.status_code == 200
    assert resp.get_json() == {"message": "Hello from Inventory API!"}


# ---------- GET /products Tests ----------
def test_get_products_empty(client) -> None:
    resp = client.get("/api/products")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_get_nonexistent_product(client) -> None:
    resp = client.get("/api/products/999")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


# ---------- POST /products Tests ----------
def test_create_and_get_product(client, base_product: Dict) -> None:
    post_resp = client.post("/api/products", json=base_product)
    assert post_resp.status_code == 201
    created = post_resp.get_json()
    assert created["product_id"] == base_product["product_id"]
    assert created["product_name"] == base_product["product_name"]

    get_resp = client.get(f"/api/products/{base_product['product_id']}")
    assert get_resp.status_code == 200
    fetched = get_resp.get_json()
    assert fetched["product_id"] == base_product["product_id"]
    assert fetched["price"] == base_product["price"]


def test_create_product_missing_json(client) -> None:
    resp = client.post("/api/products", content_type="application/json")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_create_product_invalid_data(client) -> None:
    resp = client.post("/api/products", json={"wrong_field": "oops"})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_create_product_duplicate_id(client, base_product: Dict) -> None:
    client.post("/api/products", json=base_product)
    resp = client.post("/api/products", json=base_product)
    assert resp.status_code == 409
    assert "error" in resp.get_json()


def test_create_multiple_products(
    client, base_product: Dict, second_product: Dict
) -> None:
    client.post("/api/products", json=base_product)
    client.post("/api/products", json=second_product)

    resp = client.get("/api/products")
    assert resp.status_code == 200
    all_products = resp.get_json()
    assert len(all_products) == 2
    ids = [p["product_id"] for p in all_products]
    assert base_product["product_id"] in ids
    assert second_product["product_id"] in ids


# ---------- PUT /products/<id> Tests ----------
def test_update_existing_product(client, base_product: Dict) -> None:
    client.post("/api/products", json=base_product)
    update_data = {"product_name": "Updated Name", "price": 20.5}
    resp = client.put(f"/api/products/{base_product['product_id']}", json=update_data)
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated["product_name"] == "Updated Name"
    assert updated["price"] == 20.5


def test_update_product_missing_json(client, base_product: Dict) -> None:
    client.post("/api/products", json=base_product)
    resp = client.put(
        f"/api/products/{base_product['product_id']}", content_type="application/json"
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_update_nonexistent_product(client) -> None:
    resp = client.put("/api/products/888", json={"price": 25.0})
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


def test_update_invalid_product_data(client, base_product: Dict) -> None:
    client.post("/api/products", json=base_product)
    resp = client.put(
        f"/api/products/{base_product['product_id']}", json={"quantity": "bad"}
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


# ---------- Edge Case Tests ----------
def test_negative_quantity_price(client, base_product: Dict) -> None:
    negative_product = base_product.copy()
    negative_product.update({"quantity": -1, "price": -10})
    resp = client.post("/api/products", json=negative_product)
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_partial_update_only_one_field(client, base_product: Dict) -> None:
    client.post("/api/products", json=base_product)
    update_data = {"price": 99.99}
    resp = client.put(f"/api/products/{base_product['product_id']}", json=update_data)
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated["price"] == 99.99
    assert updated["product_name"] == base_product["product_name"]


def test_empty_string_fields(client, base_product: Dict) -> None:
    bad_product = base_product.copy()
    bad_product["product_name"] = ""
    resp = client.post("/api/products", json=bad_product)
    assert resp.status_code == 400
    assert "error" in resp.get_json()


# ---------- Additional Tests for 100% Coverage ----------


def test_update_product_unexpected_exception(client, base_product: Dict):
    """Trigger unexpected exception in update_product safely using a context."""
    client.post("/api/products", json=base_product)
    with patch(
        "api.routes.inventory.Inventory.create_product_from_row",
        side_effect=Exception("Unexpected error"),
    ):
        resp = client.put(
            f"/api/products/{base_product['product_id']}", json={"price": 123}
        )
        assert resp.status_code == 500
        assert "error" in resp.get_json()


def test_create_product_unexpected_exception(client, base_product):
    """
    Trigger the generic Exception branch in create_product (line 100)
    by patching create_product_from_row to raise an unexpected error.
    """
    with patch(
        "Week3.core.Inventory.create_product_from_row",
        side_effect=Exception("Unexpected error"),
    ):
        resp = client.post("/api/products", json=base_product)
        assert resp.status_code == 500
        data = resp.get_json()
        assert data is not None
        assert "error" in data
        assert data["error"] == "Unexpected error"


def test_create_product_badrequest_exception(client):
    """
    Trigger the 'except BadRequest' branch in create_product
    by sending invalid JSON (will raise BadRequest automatically).
    """
    # Send invalid JSON (string instead of JSON object) with correct Content-Type
    resp = client.post(
        "/api/products", data="{'product_id': 'json'}", content_type="application/json"
    )

    assert resp.status_code == 400
    data = resp.get_json()
    assert data is not None
    assert "error" in data
    assert data["error"] == "Invalid or missing JSON body"
