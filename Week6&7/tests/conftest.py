import pytest
from api.app import create_app
from api.config import TestingConfig
from api.db import db


@pytest.fixture(scope="session")
def app():
    """
    Create and configure a new app instance for testing.
    Uses the TestingConfig (PostgreSQL test database).
    """
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    """
    Flask test client for making requests to the app.
    """
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
