"""Сервис авторизации через провайдеров OAuth 2.0."""
from typing import Mapping, Type
from uuid import UUID

from core.db import db
from core.exceptions import ResourceNotFoundError
from models.social_account import SocialAccount
from services.social_auth.base_provider import BaseOAuth
from services.social_auth.google_provider import GoogleOAuthService
from utils import messages as msg


class OAuthService:
    """Управление авторизацией OAuth."""

    soc_acc_model: Type[db.Model] = SocialAccount
    oauth_service: BaseOAuth

    def __init__(self, service: str):
        """Активировать OAuth провайдера.

        Если название для нас неизвестно, вернуть ошибку.
        """
        if service == 'google':
            self.oauth_service = GoogleOAuthService()
        else:
            raise ResourceNotFoundError(msg.authentication_service_not_found)

    def get_oauth_url(self):
        """Получить урл.

        На который направить юзера для авторизации у провайдера.
        """
        return self.oauth_service.get_oauth_url()

    def auth(self,
             request_url: str | None = None,
             data: Mapping[str, str] | None = None,
             ) -> SocialAccount:
        """Пытаемся авторизоваться."""
        auth_data = self.oauth_service.auth(request_url=request_url, data=data)
        return self._get_or_create_soc_acc(
            social_name=self.oauth_service.social_name,
            social_id=auth_data.social_id,
            user_id=auth_data.user_id,
        )

    def _get_or_create_soc_acc(self,
                               social_id: str,
                               social_name: str,
                               user_id: UUID,
                               ) -> SocialAccount:
        """Получить SocialAccount, если нет, создать."""
        soc_acc = self.soc_acc_model.query.filter_by(
            social_id=social_id, social_name=social_name).first()
        if not soc_acc:
            soc_acc = self.soc_acc_model(
                social_id=social_id, social_name=social_name, user_id=user_id)
            soc_acc.create()
        return soc_acc


def get_oauth_service(service: str):
    """Получить сервис OAuth."""
    return OAuthService(service=service)
