from core.config import config
from core.db import db
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from models.role import Role
from models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.flask_config)

    from core.exceptions import exceptions

    app.register_blueprint(exceptions)

    db.app = app
    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

    return app
