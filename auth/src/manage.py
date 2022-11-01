import click
from flask.cli import FlaskGroup
from flask_security.utils import hash_password

from app import create_app
from core.config import config
from core.db import db
from models import Role, User
from services.user_manager import get_user_manager_service
from utils import messages as msg

app = create_app()
cli = FlaskGroup(app)


@cli.command('create_db')
def create_db() -> None:
    """Пересоздать всю БД."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('create_superuser')
@click.argument('login')
@click.argument('password')
@click.argument('email')
def create_superuser(login: str, password: str, email: str) -> None:
    """Создать пользователя с ролью админа.

    Название роли в конфигах.
    Если роль не существует, то она создается.
    """
    password = hash_password(password)
    user_manager = get_user_manager_service(user_model=User, role_model=Role)
    new_user = user_manager.create_user(
        password=password,
        login=login,
        email=email,
    )
    role_admin = user_manager.find_or_create_role(config.admin_role_name)
    user_manager.add_role_to_user(user=new_user, role=role_admin)
    db.session.commit()
    print(msg.hello_name.format(new_user.login))
    db.session.close()


if __name__ == '__main__':
    cli()
