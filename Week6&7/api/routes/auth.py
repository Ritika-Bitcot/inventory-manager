from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from ..db import db
from ..jwt_service import JWTService
from ..models import User
from ..schemas.request import LoginRequest
from ..schemas.response import ErrorResponse, LoginResponse
from ..schemas.user import RegisterRequest

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user.

    Expected JSON payload:
    {
        "username": "example_user",
        "password": "securepassword123"
    }
    """
    try:
        # Validate request with Pydantic
        data = RegisterRequest(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    # Check if user already exists
    if User.query.filter_by(username=data.username).first():
        return jsonify({"error": "Username already taken"}), 400

    # Create new user
    user = User(username=data.username)
    user.set_password(data.password)

    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User registered successfully",
                "user": {"id": user.id, "username": user.username},
            }
        ),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates user and returns JWT access token.
    """
    try:
        data = LoginRequest(**request.get_json())
    except ValidationError as e:
        return (
            jsonify(
                ErrorResponse(error="Validation error", details=e.errors()).model_dump()
            ),
            400,
        )

    # Check user
    user = User.query.filter_by(username=data.username).first()
    if not user or not user.check_password(data.password):
        return (
            jsonify(ErrorResponse(error="Invalid username or password").model_dump()),
            401,
        )

    # Generate access token
    token = JWTService.generate_token(str(user.id), user.username)
    response = LoginResponse(access_token=token)
    return jsonify(response.model_dump()), 200
