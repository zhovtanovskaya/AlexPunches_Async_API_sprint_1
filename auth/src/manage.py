"""Запустить приложение и cli-команды."""

import click
from flask import request
from flask.cli import FlaskGroup

import services.models.users as us_models
from app import create_app
from core.config import config
from core.db import db
from services.role import get_role_service
from services.user import get_user_service
from utils import messages as msg

app = create_app()
cli = FlaskGroup(app)


@app.before_request
def before_request():
    """Не пускать запроссы без заголовка X-Request-Id.

    Чтобы ни кто не прошел мимо Jaeger.
    """
    request_id = request.headers.get('X-Request-Id')
    if config.enable_tracer and not request_id:
        raise RuntimeError('request id is required')


@cli.command('create_db')
def create_db() -> None:
    """Пересоздать всю БД."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('create_superuser')
@click.argument('password')
@click.argument('email')
def create_superuser(password: str, email: str) -> None:
    """Создать пользователя с ролью админа.

    Название роли в конфигах.
    Если роль не существует, то она создается.
    """
    user_service = get_user_service()
    role_service = get_role_service()

    new_user = user_service.register_user(us_models.UserCreateModel(
        password=password,
        email=email,
    ))
    role_admin = role_service.find_or_create_role(config.admin_role_name)
    user_service.add_role_to_user_by_rolename(user_id=new_user.id,
                                              rolename=role_admin.name)
    print(msg.hello_name.format(new_user.email))


if __name__ == '__main__':
    cli()
