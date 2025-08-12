from flask import Flask

from .routes.inventory import inventory_bp


def create_app():
    from Week3.utils import setup_logger

    setup_logger()

    app = Flask(__name__)
    app.register_blueprint(inventory_bp, url_prefix="/api")
    return app
