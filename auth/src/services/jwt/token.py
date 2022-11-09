"""Сервис для управления JWT-токенами."""
import uuid
from enum import Enum

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jti)
from pydantic import BaseModel, Field, PositiveInt

from core.config import config
from core.redis import jwt_redis_blocklist

ACCESS_EXPIRES = config.flask_config.JWT_ACCESS_TOKEN_EXPIRES


class JWTType(str, Enum):
    """Типы JWT-токенов."""

    REFRESH = 'refresh'
    ACCESS = 'access'


class RefreshPayload(BaseModel):
    """Объектное представление содержимого refresh-токена."""

    type: JWTType = Field(JWTType.REFRESH, const=True)
    jti: uuid.UUID = Field(
        description='Уникальный идентификатор refresh-токена.')
    eol: PositiveInt = Field(
        description='Конец жизни refresh-токена в виде Unix timestamp.')
    access_jti: uuid.UUID = Field(
        description='Уникальный идентификатор access-токена.')


class TokenService:
    """Сервис для создания и отзыва JWT доступа и обновления."""

    @staticmethod
    def create_tokens(username: str) -> tuple[str, str]:
        """Создать пару JWT для доступа и обновления.

        Созданный refresh JWT содержит собственный уникальный
        идентификатор 'jti', и уникальный идентификатор access JWT
        в поле 'ajti'.  Благодаря чему можно отзывать оба токена
        за один запрос при предъявлении одного лишь refresh-токена.
        """
        access_token = create_access_token(identity=username)
        claims = {'ajti': get_jti(access_token)}
        refresh_token = create_refresh_token(
            identity=username, additional_claims=claims)
        return access_token, refresh_token

    @staticmethod
    def revoke_tokens(refresh_payload: dict):
        """Отозвать JWT доступа и обновления.

        Добавить в Redis уникальный идентификатор refresh-токена,
        и уникальный идентификатор access-токена.  Таким образом
        обозначить, что до конца срока действия эти токены считать
        не действующими.

        Arguments:
            refresh_payload -- декодированное содержимое (payload) JWT.
        """
        refresh = RefreshPayload(
            type=refresh_payload['type'],
            jti=refresh_payload['jti'],
            eol=refresh_payload['exp'],
            access_jti=refresh_payload['ajti'],
        )
        # Сохранить refresh-токен в Redis до тех пор,
        # пока не истечет его срок с момента создания.
        jwt_redis_blocklist.set(str(refresh.jti), '', exat=refresh.eol)
        jwt_redis_blocklist.set(str(refresh.access_jti), '', ex=ACCESS_EXPIRES)
