import os
from flask import Flask
from flask_migrate import Migrate
from .config import Config, DevelopmentConfig
from .db import db
from .routes.web import web_bp
from .routes.api import api_bp

migrate = Migrate()


def create_app(config_class: type[Config] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class or _config_from_env())

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


def _config_from_env() -> type[Config]:
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return Config
    if env == "testing":
        return Config
    return DevelopmentConfig
