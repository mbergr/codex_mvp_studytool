import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def _default_sqlite_url() -> str:
    return f"sqlite:///{BASE_DIR / 'guitar_log.db'}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", _default_sqlite_url())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
