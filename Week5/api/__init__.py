from flask import Flask

from .routes.inventory import inventory_bp


def create_app():
    """
    Creates a Flask application.

    This function initializes a Flask app and registers the API blueprint
    to it. The logger is also set up to log errors to a file.

    Returns:
        app: The Flask application instance.
    """
    from Week3.utils import setup_logger

    setup_logger()

    app = Flask(__name__)
    app.register_blueprint(inventory_bp, url_prefix="/api")
    return app
