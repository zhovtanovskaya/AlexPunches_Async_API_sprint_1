import click
from app import create_app
from core.db import db
from flask.cli import FlaskGroup
from flask_security.utils import hash_password
from models import Role, User
from routers.v1.schemes.users import UserCreate
from services.security import get_security_service

app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db() -> None:
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("create_superuser")
@click.argument("login")
@click.argument("password")
@click.argument("email")
def create_supervisor(login: str, password: str, email: str) -> None:
    password = hash_password(password)
    user_scheme = UserCreate(
        password=password,
        login=login,
        email=email,
        is_superuser=True,
    )
    user_security = get_security_service(user_model=User, role_model=Role)
    new_user = user_security.create_user(scheme=user_scheme)
    db.session.commit()
    print(f'Hello, {new_user.login}!')
    db.session.close()


if __name__ == "__main__":
    cli()
