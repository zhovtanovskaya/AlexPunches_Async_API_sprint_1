"""Утилиты для работы с JWT из запроса."""
from functools import wraps
from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request

from core.config import config

__all__ = ['get_jwt', 'jwt_required', 'admin_required']


def admin_required():
    """Убедиться, что пользователь залогинен и это админ."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if config.admin_role_name in claims.get('roles', ()):
                return fn(*args, **kwargs)
            else:
                msg = 'Нет прав администратора.'
                return jsonify(msg=msg), HTTPStatus.FORBIDDEN
        return decorator

    return wrapper
