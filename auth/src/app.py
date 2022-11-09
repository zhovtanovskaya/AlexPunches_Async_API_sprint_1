"""Создать фабрику для приложения."""
from flask import Flask
from flask_jwt_extended import JWTManager

from core.config import config
from core.db import db


def create_app():
    """Фабрика приложения."""
    app = Flask(__name__)
    app.config.from_object(config.flask_config)

    from api.v1.roles import roles
    from api.v1.users import users
    from core.exceptions import exceptions

    app.register_blueprint(exceptions)
    app.register_blueprint(users, url_prefix='/api/v1')

    app.register_blueprint(roles, url_prefix='/api/v1')


    db.app = app
    db.init_app(app)
    app.jwt = JWTManager(app)

    return app
