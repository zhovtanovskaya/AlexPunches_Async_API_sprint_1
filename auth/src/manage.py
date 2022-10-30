import click
from flask.cli import FlaskGroup
from flask_security.utils import hash_password

from app import create_app
from core.db import db
from models import Role, User
from services.user_manager import get_user_manager_service

app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db() -> None:
    """Пересоздать всю БД."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("create_superuser")
@click.argument("login")
@click.argument("password")
@click.argument("email")
def create_superuser(login: str, password: str, email: str) -> None:
    password = hash_password(password)
    user_manager = get_user_manager_service(user_model=User, role_model=Role)
    new_user = user_manager.create_user(
        password=password,
        login=login,
        email=email,
        is_superuser=True,
    )
    db.session.commit()
    print(f'Hello, {new_user.login}!')
    db.session.close()


if __name__ == "__main__":
    cli()
