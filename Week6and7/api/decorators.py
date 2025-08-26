from functools import wraps
from typing import Any, Callable

from flask import g, jsonify, request
from jwt import ExpiredSignatureError, InvalidTokenError

from .jwt_service import JWTService


def jwt_required(fn: Callable) -> Callable:
    """
    Decorator to protect routes with JWT authentication.

    Extracts JWT from Authorization header and validates it.
    """

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Checks the Authorization header for a valid JWT token.

        If header is not present or invalid, returns a 401 error.
        If token is expired or invalid, returns a 401 error.
        Otherwise, stores the user info in the request context (g.current_user)
        and calls the wrapped function with the original arguments.
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = JWTService.validate_token(token)
            g.current_user = payload  # store user info for later use
        except ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return fn(*args, **kwargs)

    return wrapper
