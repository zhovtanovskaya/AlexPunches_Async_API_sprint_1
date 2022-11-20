"""Модуль для JWT-авторизации HTTP-запроса."""
from typing import Optional

import jwt
from fastapi import HTTPException, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, InvalidSignatureError

from auth.exceptions import AuthorizationException
from core.config import config


class AuthErrors:
    NO_TOKEN: str = 'Нет токена авторизации.'
    INVALID_SCHEME: str = 'Схема авторизации не "Bearer".'
    INVALID_TOKEN: str = 'Токен авторизации не валиден.'


class JWTBearer(HTTPBearer):
    """Проверка заголовка Authorization в HTTP-запросе.

    Методы класса проверяют, что в заголовке авторизации обязательно
    содержится валидный JWT.
    """

    def __init__(
            self,
            *,
            bearerFormat: Optional[str] = None,
            scheme_name: Optional[str] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
            secret=config.jwt_secret_key,
            algorithm=config.jwt_algorithm,
    ):
        """Инициализировать HTTPBearer и алгоритм подписи JWT-токена."""
        super().__init__(
            bearerFormat=bearerFormat,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )
        self.secret = secret
        self.algorithm = algorithm

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """Убедиться, что в запросе присутствует валидный JWT-токен."""
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request)
        if not credentials:
            raise AuthorizationException(AuthErrors.NO_TOKEN)
        if not credentials.scheme == 'Bearer':
            raise AuthorizationException(AuthErrors.INVALID_SCHEME)
        try:
            self.verify_jwt(token=credentials.credentials)
        except (DecodeError, InvalidSignatureError) as e:
            raise AuthorizationException(AuthErrors.INVALID_TOKEN) from e
        return credentials

    def verify_jwt(self, token: str):
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        print(token)
        print(payload)


jwt_bearer = JWTBearer()


async def verify_jwt_token(token: HTTPAuthorizationCredentials = Security(jwt_bearer)):
    print(token)
