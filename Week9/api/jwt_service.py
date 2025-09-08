import datetime
from typing import Any, Dict

import jwt
from flask import current_app


class JWTService:
    """
    Service class responsible for generating and validating JWT tokens.
    Adheres to SRP (only deals with JWT-related logic).
    """

    @staticmethod
    def generate_access_token(user_id: str, username: str, role: str) -> str:
        """
        Generate a JWT token for the given user.

        Args:
            user_id (str): Unique user ID.
            username (str): Username of the user.

        Returns:
            str: Encoded JWT token.
        """
        payload: Dict[str, Any] = {
            "sub": str(user_id),
            "id": str(user_id),
            "username": username,
            "role": role,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(hours=2),  # 2h expiry
        }
        secret = current_app.config.get("JWT_SECRET_KEY")
        return jwt.encode(payload, secret, algorithm="HS256")

    @staticmethod
    def generate_refresh_token(user_id: str, username: str, role: str) -> str:
        """Generate long-lived refresh token (7 days)."""
        payload: Dict[str, Any] = {
            "sub": str(user_id),
            "id": str(user_id),
            "username": username,
            "role": role,
            "type": "refresh",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        }
        secret = current_app.config.get("JWT_SECRET_KEY")
        return jwt.encode(payload, secret, algorithm="HS256")

    @staticmethod
    def validate_token(token: str) -> Dict[str, Any]:
        """
        Validate and decode a JWT token.

        Args:
            token (str): Encoded JWT.

        Returns:
            dict: Decoded payload.

        Raises:
            jwt.ExpiredSignatureError: If token expired.
            jwt.InvalidTokenError: If token invalid.
        """
        secret = current_app.config.get("JWT_SECRET_KEY")
        return jwt.decode(token, secret, algorithms=["HS256"])
