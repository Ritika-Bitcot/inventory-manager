from typing import Dict


# ---------- Basic API Endpoint Tests ----------
def test_hello_endpoint(client) -> None:
    """Test GET /hello returns a greeting message."""
    resp = client.get("/api/hello")
    assert resp.status_code == 200
    assert resp.get_json() == {"message": "Hello from Inventory API!"}


# ---------- GET /products Tests ----------
def test_get_products_empty(client) -> None:
    """Test GET /products returns empty list when inventory is empty."""
    resp = client.get("/api/products")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_get_nonexistent_product(client) -> None:
    """Test GET /products/<id> for a missing product returns 404."""
    resp = client.get("/api/products/999")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


# ---------- POST /products Tests ----------
def test_create_and_get_product(client, base_product: Dict) -> None:
    """Test POST /products creates a product and GET retrieves it correctly."""
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
    """Test POST /products without JSON body returns 400."""
    resp = client.post("/api/products", content_type="application/json")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_create_product_invalid_data(client) -> None:
    """Test POST /products with invalid product data returns 400."""
    resp = client.post("/api/products", json={"wrong_field": "oops"})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_create_product_duplicate_id(client, base_product: Dict) -> None:
    """Test creating two products with same product_id returns 409 on second."""
    client.post("/api/products", json=base_product)
    resp = client.post("/api/products", json=base_product)
    assert resp.status_code == 409
    assert "error" in resp.get_json()


def test_create_multiple_products(
    client, base_product: Dict, second_product: Dict
) -> None:
    """Test creating multiple products and fetching them all."""
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
    """Test PUT /products/<id> updates a product successfully."""
    client.post("/api/products", json=base_product)
    update_data = {"product_name": "Updated Name", "price": 20.5}
    resp = client.put(f"/api/products/{base_product['product_id']}", json=update_data)
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated["product_name"] == "Updated Name"
    assert updated["price"] == 20.5


def test_update_product_missing_json(client, base_product: Dict) -> None:
    """Test PUT /products/<id> without JSON body returns 400."""
    client.post("/api/products", json=base_product)
    resp = client.put(
        f"/api/products/{base_product['product_id']}", content_type="application/json"
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_update_nonexistent_product(client) -> None:
    """Test PUT /products/<id> for a missing product returns 404."""
    resp = client.put("/api/products/888", json={"price": 25.0})
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Product not found"


def test_update_invalid_product_data(client, base_product: Dict) -> None:
    """Test PUT /products/<id> with invalid data returns 400."""
    client.post("/api/products", json=base_product)
    resp = client.put(
        f"/api/products/{base_product['product_id']}", json={"quantity": "bad"}
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


# ---------- Edge Case Tests ----------
def test_negative_quantity_price(client, base_product: Dict) -> None:
    """Test that negative quantity or price returns 400."""
    negative_product = base_product.copy()
    negative_product.update({"quantity": -1, "price": -10})
    resp = client.post("/api/products", json=negative_product)
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_partial_update_only_one_field(client, base_product: Dict) -> None:
    """Test updating a single field while leaving others intact."""
    client.post("/api/products", json=base_product)
    update_data = {"price": 99.99}
    resp = client.put(f"/api/products/{base_product['product_id']}", json=update_data)
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated["price"] == 99.99
    assert updated["product_name"] == base_product["product_name"]


def test_empty_string_fields(client, base_product: Dict) -> None:
    """Test product_name cannot be empty."""
    bad_product = base_product.copy()
    bad_product["product_name"] = ""
    resp = client.post("/api/products", json=bad_product)
    assert resp.status_code == 400
    assert "error" in resp.get_json()
