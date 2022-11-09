"""Сервис аутентификации."""
from functools import lru_cache
from typing import Any, Mapping
from uuid import UUID

from flask import request
from werkzeug.datastructures import Authorization
from werkzeug.security import check_password_hash

import core.exceptions as core_exc
from models.user import User
from utils import messages as msg


class AuthService:
    """Класс управления аутентификацией и авторизацией."""

    def auth_user(self, auth_data: Authorization | None) -> Mapping[str, Any]:
        """Аутентифицировать пользователя по логину и паролю."""
        if not auth_data:
            raise core_exc.AuthenticateRequriedError(
                msg.could_not_verify,
                payload={'WWW-Authenticate':
                         f'Basic realm="{msg.realm_authorization_requried}"'},
            )
        if not auth_data.username:
            raise core_exc.AuthenticateRequriedError(
                msg.could_not_verify,
                payload={'WWW-Authenticate':
                         f'Basic realm="{msg.realm_login_requried}"'},
            )
        if not auth_data.password:
            raise core_exc.AuthenticateRequriedError(
                msg.could_not_verify,
                payload={'WWW-Authenticate':
                         f'Basic realm="{msg.realm_password_requried}"'},
            )

        if user := User.query.filter_by(email=auth_data.username).first():
            if check_password_hash(pwhash=user.password,
                                   password=auth_data.password,
                                   ):
                return self.make_pair_tokens_by_user_id(user_id=user.id)
            raise core_exc.AuthenticateRequriedError(
                msg.password_is_not_correct,
                payload={'WWW-Authenticate':
                         f'Basic realm="{msg.realm_password_is_not_correct}"'},
            )

        raise core_exc.AuthenticateRequriedError(
            msg.realm_user_not_found,
            payload={'WWW-Authenticate':
                     f'Basic realm="{msg.realm_user_not_found}"'},
        )

    def make_pair_tokens_by_user_id(self, user_id: UUID) -> Mapping[str, str]:
        """Создать пару токенов."""
        access_token = self.make_access_token_by_user_id(user_id=user_id)
        refresh_token = self.make_refresh_token_by_user_id(user_id=user_id)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    @staticmethod
    def make_access_token_by_user_id(user_id: UUID) -> str:
        """Создать и вернуть access_token."""
        # TODO подключить TokenService
        new_access_token = ''  # noqa
        return new_access_token

    @staticmethod
    def make_refresh_token_by_user_id(user_id: UUID) -> str:
        """Создать, обновить в БД, и вернуть refresh_token."""
        # TODO подключить TokenService
        new_refresh_token = ''  # noqa
        return new_refresh_token

    def signout_user_by_id(self, user_id: UUID):
        """Выйти пользователю."""
        return self.disable_refresh_token_by_user_id(user_id=user_id)

    def get_current_user_id(self) -> UUID | None:
        """Проваледировать токен и получить из него user_id."""
        token_decoded = self.token_validate_and_decode(token=self.get_token())
        return token_decoded.get('user_id')

    @staticmethod
    def disable_refresh_token_by_user_id(user_id: UUID) -> None:
        """Удалить refresh_token по user_id."""
        # TODO подключить TokenService
        return None

    @staticmethod
    def get_token():
        """Получить токен посетителя."""
        return request.headers.get('x-access-token')

    @staticmethod
    def token_validate_and_decode(token: str) -> Mapping[str, Any]:
        """Декодировать и валидировать токен."""
        return {'': None}


@lru_cache()
def get_auth_service() -> AuthService:
    """Создать и/или вернуть синглтон AuthService."""
    return AuthService()
