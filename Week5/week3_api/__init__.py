from flask import Flask

from .routes.inventory import inventory_bp


def create_app():
    """
    Creates a Flask app.

    This function is the app factory. It is the entry point for the
    Flask application. It is used to create the Flask app, and register
    the blueprint for the inventory API.

    Returns:
        Flask: The Flask app.
    """
    app = Flask(__name__)
    app.register_blueprint(inventory_bp, url_prefix="/api")
    return app
