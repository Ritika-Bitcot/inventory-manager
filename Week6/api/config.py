import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ.get('DB_USER', 'postgres')}:"
        f"{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}:"
        f"{os.environ.get('DB_PORT')}/"
        f"{os.environ.get('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ.get('DB_USER', 'postgres')}:"
        f"{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}:"
        f"{os.environ.get('DB_PORT')}/"
        f"{os.environ.get('TEST_DB_NAME')}"
    )
    TESTING = True
