"""Модуль для JWT-авторизации HTTP-запроса."""
from typing import Optional
from uuid import UUID

import jwt
from pydantic import BaseModel, Field

from core.config import config, logger
from utils import messages as msg


class AuthorizationException(Exception):
    """Исключение об отказе в авторизации."""

    ...


class AccessTokenPayload(BaseModel):
    """Ожидаемый формат данных в токене авторизации JWT."""

    user_id: Optional[UUID] = None
    roles: list[str]
    type: str = Field('access', const=True)


def decode_jwt(token: str) -> AccessTokenPayload | None:
    """Декодировать и провалидировать полезную нагрузку JWT."""
    try:
        payload = jwt.decode(
            token,
            config.jwt_secret_key,
            algorithms=[config.jwt_algorithm],
        )
        return AccessTokenPayload(**payload)
    except Exception as e:
        logger.warn(f'{msg.token_is_invalid}: {e}')
    return None
