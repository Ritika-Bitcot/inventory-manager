import logging
import os
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

from Week3.core import Inventory

inventory_bp = Blueprint("inventory", __name__)

# CSV file path relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(
    os.path.join(base_dir, "..", "..", "..", "Week3", "data", "products.csv")
)

# Initialize inventory and load products from CSV
inventory = Inventory()
inventory.load_from_csv(csv_path)


@inventory_bp.route("/hello", methods=["GET"])
def hello() -> Tuple[Any, int]:
    """
    A simple test endpoint to verify the API is running.

    Returns:
        JSON response with message and status 200.
    """
    return jsonify({"message": "Hello from Inventory API!"}), 200


@inventory_bp.route("/products", methods=["GET"])
def get_products() -> Tuple[Any, int]:
    """
    Returns all products in the inventory.

    Returns:
        JSON response with a list of products and status 200.
    """
    products_list = [product.model_dump() for product in inventory.products if product]
    return jsonify(products_list), 200


@inventory_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> Tuple[Any, int]:
    """
    Get a specific product by product_id.

    Args:
        product_id (int): ID of the product to retrieve.

    Returns:
        JSON response with product details and status 200 if found,
        else error message and status 404.
    """
    product = next((p for p in inventory.products if p.product_id == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.model_dump()), 200


@inventory_bp.route("/products", methods=["POST"])
def create_product() -> Tuple[Any, int]:
    """
    Create a new product in the inventory.

    Returns:
        JSON response with created product and status 201 if successful,
        else error message with 400/409/500.
    """
    try:
        product_data = request.get_json()
        breakpoint()

        if not product_data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        product = inventory.create_product_from_row(product_data)
        if product is None:
            return jsonify({"error": "Invalid product data"}), 400

        if any(p.product_id == product.product_id for p in inventory.products):
            return (
                jsonify({"error": "Product with this product_id already exists"}),
                409,
            )

        inventory.products.append(product)
        return jsonify(product.model_dump()), 201

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    except BadRequest:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    except Exception as e:
        logging.error(f"Unexpected error in create_product: {e}")
        return jsonify({"error": str(e)}), 500


@inventory_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> Tuple[Any, int]:
    """
    Update an existing product by product_id.

    Args:
        product_id (int): ID of the product to update.

    Returns:
        JSON response with updated product and status 200 if successful,
        else error message with 400/404/500.
    """
    try:
        update_data = request.get_json(silent=True)
        if not update_data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        # Find index of existing product
        idx = next(
            (i for i, p in enumerate(inventory.products) if p.product_id == product_id),
            None,
        )
        if idx is None:
            return jsonify({"error": "Product not found"}), 404

        # Merge existing product data with updates
        existing_product = inventory.products[idx]
        updated_dict = existing_product.model_dump()
        updated_dict.update(update_data)

        # Validate updated product
        updated_product = inventory.create_product_from_row(updated_dict)
        if updated_product is None:
            return jsonify({"error": "Invalid updated data"}), 400

        # Replace old product
        inventory.products[idx] = updated_product
        return jsonify(updated_product.model_dump()), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        logging.error(f"Unexpected error in update_product: {e}")
        return jsonify({"error": "Internal server error"}), 500
