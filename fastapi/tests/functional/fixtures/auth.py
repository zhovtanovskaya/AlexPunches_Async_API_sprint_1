"""Утилиты для авторизации пользователей в тестах."""

import jwt
import pytest_asyncio

from functional.settings import test_settings


@pytest_asyncio.fixture(scope='function')
async def access_token():
    """Создать JWT access-токен для авторизации."""
    return jwt.encode(
        test_settings.jwt_access_payload,
        test_settings.jwt_secret_key,
        test_settings.jwt_algorithm,
    )
