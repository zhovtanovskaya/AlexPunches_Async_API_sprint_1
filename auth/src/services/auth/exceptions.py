"""Исключения аутентификации и авторизации."""

from http import HTTPStatus

from core.exceptions import BasicExceptionError


class AuthenticationFailed(BasicExceptionError):
    """Аутентификация не удалась."""

    def __init__(self, message: str):
        """Инициализировать исключение с HTTP-кодом 422."""
        super().__init__(message, HTTPStatus.UNPROCESSABLE_ENTITY)
