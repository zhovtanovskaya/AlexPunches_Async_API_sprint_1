"""Утилиты для работы с JWT из запроса."""

from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, Union

from flask import Response, jsonify
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request

from core.config import config

__all__ = ['get_jwt', 'jwt_required', 'admin_required']

C = Callable[..., Union[Response, tuple[Response, HTTPStatus]]]


def admin_required():
    """Убедиться, что пользователь залогинен и это админ."""
    def decorator(controller: C) -> C:
        @wraps(controller)
        def wrapper(
                *args: Any, **kwargs: Any,
                ) -> Union[Response, tuple[Response, HTTPStatus]]:
            verify_jwt_in_request()
            claims = get_jwt()
            if config.admin_role_name in claims.get('roles', ()):
                return controller(*args, **kwargs)
            else:
                msg = 'Нет прав администратора.'
                return jsonify(msg=msg), HTTPStatus.FORBIDDEN

        return wrapper

    return decorator
