from flask import Blueprint, jsonify, request
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import ValidationError

from ..db import db
from ..jwt_service import JWTService
from ..models import User
from ..schemas.request import LoginRequest
from ..schemas.response import ErrorResponse, LoginResponse, RefreshResponse
from ..schemas.user import RegisterRequest

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register() -> tuple:
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
    user = User(username=data.username, role=data.role)
    user.set_password(data.password)

    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User registered successfully",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "role": user.role,
                },
            }
        ),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login() -> tuple:
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

    # Generate token
    access_token = JWTService.generate_access_token(
        str(user.id), user.username, user.role
    )
    refresh_token = JWTService.generate_refresh_token(
        str(user.id), user.username, user.role
    )

    response = LoginResponse(access_token=access_token, refresh_token=refresh_token)

    return jsonify(response.model_dump()), 200


@auth_bp.route("/refresh", methods=["POST"])
def refresh() -> tuple:
    """
    Refreshes an access token given a valid refresh token.

    Returns a new access token and a new refresh token.
    If the refresh token is invalid or expired, returns a 401 error.
    """
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify(ErrorResponse(error="Refresh token required").model_dump()), 400

    try:
        payload = JWTService.validate_token(refresh_token)

        if payload.get("type") != "refresh":
            return jsonify(ErrorResponse(error="Invalid token type").model_dump()), 401

        access_token = JWTService.generate_access_token(
            payload["sub"], payload["username"], payload
        )
        refresh_token = JWTService.generate_refresh_token(
            payload["sub"], payload["username"], payload["role"]
        )
        response = RefreshResponse(
            access_token=access_token, refresh_token=refresh_token
        )
        return jsonify(response.model_dump()), 200

    except ExpiredSignatureError:
        return jsonify(ErrorResponse(error="Refresh token expired").model_dump()), 401
    except InvalidTokenError:
        return jsonify(ErrorResponse(error="Invalid refresh token").model_dump()), 401
