import os

from flask import Blueprint, jsonify

from Week3.core import Inventory

inventory_bp = Blueprint("inventory", __name__)

# Calculate absolute CSV path relative to this file for portability

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(
    os.path.join(base_dir, "..", "..", "..", "Week3", "data", "products.csv")
)


# Initialize the Inventory instance and load CSV once
inventory = Inventory()
inventory.load_from_csv(csv_path)


@inventory_bp.route("/hello", methods=["GET"])
def hello() -> tuple:
    """
    Simple test endpoint to check if the API is running.

    Returns:
        tuple: JSON response with a friendly message and HTTP status code 200.
    """
    return jsonify({"message": "Hello from Inventory API!"}), 200


@inventory_bp.route("/products", methods=["GET"])
def get_products() -> tuple:
    """
    Returns a list of all products in the inventory.

    Returns:
        tuple: JSON response with a list of products and HTTP status code 200.
    """
    products_list = [product.dict() for product in inventory.products if product]
    return jsonify(products_list), 200


@inventory_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> tuple:
    """
    Retrieves a specific product from the inventory by its product ID.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        tuple: A JSON response containing the product details and HTTP status code 200
        if found, or an error message and HTTP status code 404 if not found.
    """

    product = next((p for p in inventory.products if p.product_id == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.dict()), 200
