from auth_models.role import Role
from auth_models.user import User
from core.config import config
from core.db import db
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.flask_config)

    from core.exceptions import exceptions
    from routers.v1.auth import auth
    from routers.v1.roles import roles
    from routers.v1.users import users

    app.register_blueprint(exceptions)
    app.register_blueprint(auth, url_prefix='/auth/v1')
    app.register_blueprint(users, url_prefix='/auth/v1')
    app.register_blueprint(roles, url_prefix='/auth/v1')

    db.app = app
    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

    return app
