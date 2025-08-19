from typing import Any, Dict, Type

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..db import db
from ..models import BookProduct, ElectronicProduct, FoodProduct, Product
from ..schemas import (
    BookProductCreate,
    ElectronicProductCreate,
    FoodProductCreate,
    ProductUpdate,
)

bp = Blueprint("products", __name__, url_prefix="/api/products")

CATEGORY_MAP: Dict[str, Type[Product]] = {
    "food": FoodProduct,
    "electronic": ElectronicProduct,
    "book": BookProduct,
}


SCHEMA_MAP: Dict[str, Type] = {
    "food": FoodProductCreate,
    "electronic": ElectronicProductCreate,
    "book": BookProductCreate,
}


@bp.route("/", methods=["GET"])
def get_products() -> tuple[Any, int]:
    """
    Fetch all products from the database.

    Returns:
        JSON response containing a list of all products with HTTP status code 200,
        or an error message with status 500 in case of a database error.
    """
    try:
        products = Product.query.all()
        return jsonify([p.serialize() for p in products]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


@bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> tuple[Any, int]:
    """
    Fetch a single product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        JSON response containing the product data with HTTP status 200,
        404 if the product does not exist,
        or 500 if a database error occurs.
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product.serialize()), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


@bp.route("/", methods=["POST"])
def create_product() -> tuple[Any, int]:
    """
    Create a new product in the database.

    Expects a JSON payload matching one of the schema definitions in SCHEMA_MAP.

    Returns:
        JSON response containing the created product data and HTTP status 201,
        400 for validation or integrity errors,
        or 500 for database errors.
    """
    try:
        data: Dict[str, Any] = request.get_json()
        category = data.get("category", "").lower()
        if category not in SCHEMA_MAP:
            return jsonify({"error": "Invalid category"}), 400

        schema_class = SCHEMA_MAP[category]
        product_data = schema_class(**data)

        model_class = CATEGORY_MAP[category]
        product = model_class(**product_data.dict())

        db.session.add(product)
        db.session.commit()
        return (
            jsonify({"message": "Product created", "product": product.serialize()}),
            201,
        )
    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Integrity error", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


@bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> tuple[Any, int]:
    """
    Update an existing product by its ID.

    Expects a JSON payload matching ProductUpdate schema.

    Args:
        product_id (int): ID of the product to update.

    Returns:
        JSON response containing the updated product and HTTP status 200,
        404 if the product does not exist,
        400 for validation or integrity errors,
        or 500 for database errors.
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        data: Dict[str, Any] = request.get_json()
        update_data = ProductUpdate(**data)

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(product, key, value)

        db.session.commit()
        return (
            jsonify({"message": "Product updated", "product": product.serialize()}),
            200,
        )
    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Integrity error"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


@bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int) -> tuple[Any, int]:
    """
    Delete a product from the database by its ID.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        JSON response with message of successful deletion and HTTP status 200,
        404 if the product does not exist,
        or 500 if a database error occurs.
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
