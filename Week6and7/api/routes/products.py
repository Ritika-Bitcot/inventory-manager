from typing import Any, Dict, Type

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from api.schemas.request import (
    BookProductCreate,
    ElectronicProductCreate,
    FoodProductCreate,
    ProductUpdate,
)
from api.schemas.response import (
    ErrorResponse,
    ProductCreateResponse,
    ProductDeleteResponse,
    ProductResponse,
    ProductUpdateResponse,
)

from ..db import db
from ..decorators import jwt_required, roles_required
from ..models import BookProduct, ElectronicProduct, FoodProduct, Product

bp = Blueprint("productSs", __name__, url_prefix="/api/products")

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
@roles_required("staff", "manager", "admin")
def get_products() -> tuple[Any, int]:
    """
    Fetch all products from the database.

    Returns:
        JSON response containing a list of all products with HTTP status code 200,
        or an error message with status 500 in case of a database error.
    """
    try:
        products = Product.query.all()
        response = [ProductResponse.model_validate(p).model_dump() for p in products]
        return jsonify({"products": response}), 200
    except SQLAlchemyError as e:
        return (
            jsonify(ErrorResponse(error="Database error", details=str(e)).model_dump()),
            500,
        )


@bp.route("/<int:product_id>", methods=["GET"])
@roles_required("staff", "manager", "admin")
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
            return jsonify(ErrorResponse(error="Product not found").model_dump()), 404
        return jsonify(ProductResponse.model_validate(product).model_dump()), 200
    except SQLAlchemyError as e:
        return (
            jsonify(ErrorResponse(error="Database error", details=str(e)).model_dump()),
            500,
        )


@bp.route("/", methods=["POST"])
@roles_required("manager", "admin")
@jwt_required
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
            return jsonify(ErrorResponse(error="Invalid category").model_dump()), 400

        schema_class = SCHEMA_MAP[category]
        product_data = schema_class(**data)

        model_class = CATEGORY_MAP[category]
        # Add current user as product owner
        from flask import g

        current_user = g.current_user
        product = model_class(**product_data.model_dump(), owner_id=current_user["sub"])

        db.session.add(product)
        db.session.commit()

        return (
            jsonify(
                ProductCreateResponse(
                    message="Product created",
                    product=ProductResponse.model_validate(product),
                ).model_dump()
            ),
            201,
        )
    except ValidationError as e:
        return (
            jsonify(
                ErrorResponse(error="Validation error", details=e.errors()).model_dump()
            ),
            400,
        )
    except IntegrityError as e:
        db.session.rollback()
        return (
            jsonify(
                ErrorResponse(error="Integrity error", details=str(e)).model_dump()
            ),
            400,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return (
            jsonify(ErrorResponse(error="Database error", details=str(e)).model_dump()),
            500,
        )


@bp.route("/<int:product_id>", methods=["PUT"])
@roles_required("manager", "admin")
@jwt_required
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
            return jsonify(ErrorResponse(error="Product not found").model_dump()), 404
        from flask import g

        current_user = g.current_user

        # Restrict managers from editing other manager’s products
        if (
            current_user["role"] == "manager"
            and str(product.owner_id) != current_user["sub"]
        ):
            return (
                jsonify(
                    {"error": "Forbidden: cannot modify another manager's product"}
                ),
                403,
            )

        data: Dict[str, Any] = request.get_json()
        update_data = ProductUpdate(**data)

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        db.session.commit()
        return (
            jsonify(
                ProductUpdateResponse(
                    message="Product updated",
                    product=ProductResponse.model_validate(product),
                ).model_dump()
            ),
            200,
        )

    except ValidationError as e:
        return (
            jsonify(
                ErrorResponse(error="Validation error", details=e.errors()).model_dump()
            ),
            400,
        )
    except IntegrityError as e:
        db.session.rollback()
        return (
            jsonify(
                ErrorResponse(error="Integrity error", details=str(e)).model_dump()
            ),
            400,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return (
            jsonify(ErrorResponse(error="Database error", details=str(e)).model_dump()),
            500,
        )


@bp.route("/<int:product_id>", methods=["DELETE"])
@roles_required("admin")
@jwt_required
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
            return jsonify(ErrorResponse(error="Product not found").model_dump()), 404
        db.session.delete(product)
        db.session.commit()
        return (
            jsonify(ProductDeleteResponse(message="Product deleted").model_dump()),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return (
            jsonify(ErrorResponse(error="Database error", details=str(e)).model_dump()),
            500,
        )
