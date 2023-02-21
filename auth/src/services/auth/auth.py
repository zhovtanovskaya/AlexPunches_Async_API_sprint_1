"""Модуль с утилитами для аутентификации и авторизации."""
from uuid import UUID

from flask import url_for
from werkzeug.security import check_password_hash

from core.config import config
from models.user import User
from services.auth.exceptions import AuthenticationFailed


def authenticate(email: str, password: str):
    """Убедиться, что пользователь существует и пароль верен.

    Raises:
        AuthenticationFailed: Пользователь не найден или пароль не верен.
    """
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise AuthenticationFailed('Email не верен.')
    if not check_password_hash(user.password, password):
        raise AuthenticationFailed('Пароль не верен.')


def get_comfirm_email_url_by_user(
          user: User,
          back_url: str = config.redirect_confirm,
) -> str | None:
    """Получить конфирм-урл для юзера."""
    code = user.confirmation_code
    if code is None:
        return None
    base_confirm_url = url_for('auth.confirmation_registration')
    back_url = back_url
    return f'{base_confirm_url}?code={code}&back_url={back_url}'


def email_confirmate(code: UUID) -> bool:
    """Подтвердить email."""
    if user := User.query.filter_by(confirmation_code=code).first():
        user.email_confirmation = True
        user.confirmation_code = None
        user.save()
        return True
    return False
