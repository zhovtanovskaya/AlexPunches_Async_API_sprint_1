"""Создать фабрику для приложения."""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate

from api.v1.auth import auth
from api.v1.login_histories import login_histories
from api.v1.profile import profile
from api.v1.roles import roles
from api.v1.users import users
from core.config import config
from core.db import db
from core.exceptions import exceptions


def create_app():
    """Фабрика приложения."""
    app = Flask(__name__)
    app.config.from_object(config.flask_config)
    app.register_blueprint(exceptions)
    app.register_blueprint(users, url_prefix='/api/v1')
    app.register_blueprint(roles, url_prefix='/api/v1')
    app.register_blueprint(auth, url_prefix='/api/v1')
    app.register_blueprint(login_histories, url_prefix='/api/v1')
    app.register_blueprint(profile, url_prefix='/api/v1')
    db.app = app
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    app.jwt = JWTManager(app)
    Limiter(
        app,
        key_func=get_remote_address,
        default_limits=['3 per second'],
        storage_uri='memory://',
    )
    return app
