from unittest.mock import patch

from api.jwt_service import JWTService
from jwt import ExpiredSignatureError, InvalidTokenError


# ----------------------
# REGISTER
# ----------------------
def test_register_success(client, db_session) -> None:
    """Successfully register a new user."""
    payload = {"username": "newuser", "password": "securepass", "role": "admin"}
    resp = client.post("/auth/register", json=payload)
    data = resp.get_json()
    assert resp.status_code == 201
    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "newuser"
    assert data["user"]["role"] == "admin"


def test_register_existing_username(client, test_user) -> None:
    """Register fails if username already exists."""
    payload = {
        "username": test_user.username,
        "password": "securepass",
        "role": "admin",
    }
    resp = client.post("/auth/register", json=payload)
    data = resp.get_json()
    assert resp.status_code == 400
    assert data["error"] == "Username already taken"


def test_register_validation_error(client) -> None:
    """Register fails if validation fails (password too short)."""
    payload = {"username": "user1", "password": "pass", "role": "admin"}
    resp = client.post("/auth/register", json=payload)
    data = resp.get_json()
    assert resp.status_code == 400
    assert "password" in str(data["error"][0]["loc"])


# ----------------------
# LOGIN
# ----------------------
def test_login_success(client, test_user, db_session) -> None:
    """Login returns access and refresh tokens."""
    test_user.set_password("mypassword")
    db_session.commit()

    payload = {"username": test_user.username, "password": "mypassword"}
    resp = client.post("/auth/login", json=payload)
    data = resp.get_json()
    assert resp.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_credentials(client, test_user, db_session) -> None:
    """Login fails with wrong password."""
    test_user.set_password("correctpass")
    db_session.commit()

    payload = {"username": test_user.username, "password": "wrongpass"}
    resp = client.post("/auth/login", json=payload)
    data = resp.get_json()
    assert resp.status_code == 401
    assert data["error"] == "Invalid username or password"


def test_login_validation_error(client) -> None:
    """Login fails if payload validation fails (missing password)."""
    payload = {"username": "someone"}
    resp = client.post("/auth/login", json=payload)
    data = resp.get_json()
    assert resp.status_code == 400
    assert "password" in str(data["details"][0]["loc"])


# ----------------------
# REFRESH
# ----------------------
def test_refresh_success(client) -> None:
    """Refresh token returns new access and refresh tokens."""
    # generate a refresh token with correct role
    refresh_token = JWTService.generate_refresh_token("123", "user1", "admin")
    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    data = resp.get_json()
    assert resp.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_missing_token(client) -> None:
    """Refresh fails if token not provided."""
    resp = client.post("/auth/refresh", json={})
    data = resp.get_json()
    assert resp.status_code == 400
    assert data["error"] == "Refresh token required"


def test_refresh_invalid_token_type(client) -> None:
    """Refresh fails if token type is not 'refresh'."""
    access_token = JWTService.generate_access_token("123", "user1", "admin")
    resp = client.post("/auth/refresh", json={"refresh_token": access_token})
    data = resp.get_json()
    assert resp.status_code == 401
    assert data["error"] == "Invalid token type"


def test_refresh_expired_token(client) -> None:
    """Refresh fails if token is expired."""
    with patch(
        "api.jwt_service.JWTService.validate_token", side_effect=ExpiredSignatureError
    ):
        resp = client.post("/auth/refresh", json={"refresh_token": "anytoken"})
        data = resp.get_json()
        assert resp.status_code == 401
        assert data["error"] == "Refresh token expired"


def test_refresh_invalid_token(client) -> None:
    """Refresh fails if token is invalid."""
    with patch(
        "api.jwt_service.JWTService.validate_token", side_effect=InvalidTokenError
    ):
        resp = client.post("/auth/refresh", json={"refresh_token": "anytoken"})
        data = resp.get_json()
        assert resp.status_code == 401
        assert data["error"] == "Invalid refresh token"
