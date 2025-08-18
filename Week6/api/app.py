from flask import Flask

from .config import BaseConfig
from .db import db, migrate


def create_app(config_class=BaseConfig):
    """
    Creates a Flask application with the specified configuration.

    Args:
        config_class (BaseConfig): The configuration class to use for the application.
            Defaults to BaseConfig.

    Returns:
        Flask: The created Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # import models so Alembic sees them
    from . import models
    from .routes import products

    print(models)

    app.register_blueprint(products.bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
