"""Сервис для управления JWT-токенами."""

from flask_jwt_extended import create_access_token, create_refresh_token


class TokenService:
    """Сервис для создания и отзыва JWT-токенов доступа и обновления."""

    @staticmethod
    def create_tokens(username: str) -> tuple[str, str]:
        """Создать пару JWT-токенов для доступа и обновления."""
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return access_token, refresh_token
