"""Исключения для авторизации и аутентификации."""

from http import HTTPStatus
from typing import Any, Optional

from fastapi import HTTPException


class AuthorizationException(HTTPException):
    """Исключение об отказе в авторизации."""

    def __init__(
            self,
            detail: Any = None,
            headers: Optional[dict[str, Any]] = None,
    ):
        """Инициализировать исключение со статусом HTTPStatus.FORBIDDEN."""
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN,
            detail=detail,
            headers=headers,
        )
