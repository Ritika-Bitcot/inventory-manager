import logging
import os
import sys

import psycopg2
from api.config import BaseConfig
from api.db import db
from flask import Flask
from psycopg2.extensions import connection, cursor


def connect_db() -> tuple[connection, cursor]:
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        return conn, conn.cursor()
    except psycopg2.Error as e:
        logging.error("❌ Database connection failed: %s", e)
        sys.exit(1)


def init_flask_app():
    """Initialize Flask app with SQLAlchemy."""
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    db.init_app(app)
    return app, db
