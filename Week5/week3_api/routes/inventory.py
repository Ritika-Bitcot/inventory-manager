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
def hello():
    return jsonify({"message": "Hello from Inventory API!"}), 200


@inventory_bp.route("/products", methods=["GET"])
def get_products():
    products_list = [product.dict() for product in inventory.products if product]
    return jsonify(products_list), 200


@inventory_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in inventory.products if p.product_id == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.dict()), 200
