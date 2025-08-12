import logging
import os

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

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


@inventory_bp.route("/products", methods=["POST"])
def create_product():
    """
    Creates a new product in the inventory.

    Accepts a JSON payload containing the product details.

    Returns:
        tuple: A JSON response containing the created product details and HTTP status code 201
        if successful, or an error message and HTTP status code 400/500 if not successful.
    """
    try:
        product_data = request.get_json()
        if not product_data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        product = inventory.create_product_from_row(product_data)
        if product is None:
            return jsonify({"error": "Invalid product data"}), 400

        # Check for duplicate product_id
        if any(p.product_id == product.product_id for p in inventory.products):
            return (
                jsonify({"error": "Product with this product_id already exists"}),
                409,
            )

        inventory.products.append(product)
        return jsonify(product.dict()), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        logging.error(f"Unexpected error in create_product: {e}")
        return jsonify({"error": "Internal server error"}), 500


@inventory_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> tuple:
    """
    Updates a specific product in the inventory by its product ID.

    Args:
        product_id (int): The ID of the product to update.

    Returns:
        tuple: A JSON response containing the updated
        product details and HTTP status code 200
        if found and updated, or an error message and
        HTTP status code 404/400/500 if not successful.
    """
    try:
        update_data = request.get_json()
        if not update_data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        # Find existing product index
        idx = next(
            (i for i, p in enumerate(inventory.products) if p.product_id == product_id),
            None,
        )
        if idx is None:
            return jsonify({"error": "Product not found"}), 404

        # Merge existing product data with update_data
        existing_product = inventory.products[idx]
        updated_dict = existing_product.dict()
        updated_dict.update(update_data)

        # Validate updated product by recreating Product instance
        updated_product = inventory.create_product_from_row(updated_dict)
        if updated_product is None:
            return jsonify({"error": "Invalid updated data"}), 400

        # Replace old product
        inventory.products[idx] = updated_product
        return jsonify(updated_product.dict()), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        logging.error(f"Unexpected error in update_product: {e}")
        return jsonify({"error": "Internal server error"}), 500
