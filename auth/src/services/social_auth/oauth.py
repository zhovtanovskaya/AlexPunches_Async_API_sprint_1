"""Сервис авторизации через провайдеров OAuth 2.0."""
from typing import Mapping

import services.social_auth as social_auth
from core.exceptions import ResourceNotFoundError
from db.postgres import db
from services.social_account import SocialAccountService
from utils import messages as msg

maper_oauth_providers = {
    'google': social_auth.GoogleOAuthProvider(),
}


class OAuthService:
    """Управление авторизацией OAuth."""

    soc_acc_service: SocialAccountService = SocialAccountService()
    oauth_service: social_auth.BaseOAuth

    def __init__(self, service: str):
        """Активировать OAuth провайдера.

        Если название для нас неизвестно, вернуть ошибку.
        """
        try:
            self.oauth_service = maper_oauth_providers[service]
        except KeyError:
            raise ResourceNotFoundError(msg.authentication_service_not_found)

    def get_oauth_url(self):
        """Получить урл.

        На который направить юзера для авторизации у провайдера.
        """
        return self.oauth_service.get_oauth_url()

    def auth(self,
             request_url: str | None = None,
             data: Mapping[str, str] | None = None,
             ) -> db.Model:
        """Пытаемся авторизоваться."""
        auth_data = self.oauth_service.auth(request_url=request_url, data=data)
        soc_acc = self.soc_acc_service.get_or_create_soc_acc(
            social_name=self.oauth_service.social_name,
            social_id=auth_data.social_id,
            user_id=auth_data.user_id,
        )
        return soc_acc.user


def get_oauth_service(service: str):
    """Получить сервис OAuth."""
    return OAuthService(service=service)
