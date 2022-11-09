"""Сервис для управления JWT-токенами."""

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jti)

from core.config import config
from core.redis import jwt_redis_blocklist

ACCESS_EXPIRES = config.flask_config.JWT_ACCESS_TOKEN_EXPIRES


class TokenService:
    """Сервис для создания и отзыва JWT-токенов доступа и обновления."""

    @staticmethod
    def create_tokens(username: str) -> tuple[str, str]:
        """Создать пару JWT-токенов для доступа и обновления.

        Созданный refresh JWT содержит собственный уникальный
        идентификатор 'jti', и уникальный идентификатор access JWT
        в поле 'ajti'.  Благодаря чему можно отзывать оба токена
        за один запрос при доступе по refresh-токену.
        """
        access_token = create_access_token(identity=username)
        claims = {'ajti': get_jti(access_token)}
        refresh_token = create_refresh_token(
            identity=username, additional_claims=claims)
        return access_token, refresh_token

    @staticmethod
    def revoke_tokens(jwt_payload: dict):
        """Отозвать JWT-токен доступа или обновления."""
        jti = jwt_payload['jti']
        jwt_redis_blocklist.set(jti, '', ex=ACCESS_EXPIRES)
