from dotenv import load_dotenv
from flask import Flask

from .config import BaseConfig
from .db import db, migrate

load_dotenv()


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
    from .routes import auth, chat, products

    app.logger.info(f"Imported models: {models}")

    app.register_blueprint(products.bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(chat.chat_bp)

    return app


app = create_app(BaseConfig)

if __name__ == "__main__":
    app.run(debug=True)
