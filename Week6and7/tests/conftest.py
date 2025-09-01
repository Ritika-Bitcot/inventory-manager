import random
import string
import uuid

import pytest
from api.app import create_app
from api.config import TestingConfig
from api.db import db
from api.jwt_service import JWTService
from api.models import User


@pytest.fixture(scope="session")
def app():
    """
    Create and configure a new app instance for testing.
    Uses the TestingConfig (PostgreSQL test database).
    """
    app = create_app(TestingConfig)
    app.config["JWT_SECRET_KEY"] = "test-secret"  # required for JWTService

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    """Flask test client for making requests to the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """
    Provide a clean database session for each test function.
    Rolls back any changes after the test finishes.
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection)
    db.session.configure(**options)

    yield db.session

    transaction.rollback()
    connection.close()
    db.session.remove()


# ----------------------
# User Fixtures
# ----------------------


@pytest.fixture
def test_user(db_session):
    """
    Create a test user with role=admin by default.
    """
    random_suffix = "".join(random.choices(string.ascii_lowercase, k=6))
    user = User(
        id=uuid.uuid4(),
        username=f"adminuser_{random_suffix}",
        password_hash="$2b$12$ABCDEFGHIJKLMNOPQRSTUV",  # dummy hash
        role="admin",
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def staff_user(db_session):
    """
    Create a staff role user.
    """
    random_suffix = "".join(random.choices(string.ascii_lowercase, k=6))
    user = User(
        id=uuid.uuid4(),
        username=f"staffuser_{random_suffix}",
        password_hash="$2b$12$ABCDEFGHIJKLMNOPQRSTUV",
        role="staff",
    )
    db_session.add(user)
    db_session.commit()
    return user


# ----------------------
# Auth Header Fixtures
# ----------------------


@pytest.fixture
def auth_header(test_user, app):
    """Generate Authorization header for default admin test user."""
    with app.app_context():
        token = JWTService.generate_access_token(
            user_id=str(test_user.id),
            username=test_user.username,
            role=test_user.role,
        )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def staff_auth_header(staff_user, app):
    """Authorization header for staff user."""
    with app.app_context():
        token = JWTService.generate_access_token(
            user_id=str(staff_user.id),
            username=staff_user.username,
            role=staff_user.role,
        )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_auth_header(test_user, app):
    """Authorization header for admin user."""
    with app.app_context():
        token = JWTService.generate_access_token(
            user_id=str(test_user.id),
            username=test_user.username,
            role=test_user.role,
        )
    return {"Authorization": f"Bearer {token}"}
