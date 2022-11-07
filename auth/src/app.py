"""Создать фабрику для приложения."""

from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore

from core.config import config
from core.db import db


def create_app():
    """Фабрика приложения."""
    app = Flask(__name__)
    app.config.from_object(config.flask_config)

    from api.v1.users import users
    from core.exceptions import exceptions

    app.register_blueprint(exceptions)
    app.register_blueprint(users, url_prefix='/auth/v1')

    db.app = app
    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(
        db=db, user_model=config.user_model, role_model=config.role_model,
    )
    app.security = Security(app, user_datastore)

    return app
