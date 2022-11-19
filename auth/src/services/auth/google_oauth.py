"""Сервис авторизации Google OAuth 2.0."""
from typing import Type
from uuid import UUID

import google_auth_oauthlib.flow
from googleapiclient.discovery import build

from core.config import config, logger
from core.db import db
from models.social_account import SocialAccount
from models.user import User
from services.auth.exceptions import AuthenticationFailed
from services.user import get_user_service
from utils import messages as msg

user_service = get_user_service()


class GoogleOAuthService:
    """Управление авторизацией Гуловским OAuth."""

    user_model: Type[db.Model] = User
    soc_acc_model: Type[db.Model] = SocialAccount
    social_name: str = 'google_oauth'

    @staticmethod
    def get_authorization_url() -> tuple[str, str]:
        """Получить урл гугла, на котором юзер даст разрешения."""
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=config.google_oauth,
            scopes=[
                'openid', 'https://www.googleapis.com/auth/userinfo.email'],
        )
        flow.redirect_uri = config.google_oauth_endpoint
        return flow.authorization_url(
            access_type='offline', include_granted_scopes='true',
        )

    def auth_by_request_url(self,
                            request_url: str,
                            ) -> SocialAccount:
        """Авторизовать пользователя по колбеку от Гугла."""
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=config.google_oauth,
            scopes=[
                'openid', 'https://www.googleapis.com/auth/userinfo.email'],
        )
        flow.redirect_uri = config.google_oauth_endpoint
        try:
            flow.fetch_token(authorization_response=request_url)
        except Exception as e:
            logger.error(msg.authentication_failed, exc_info=True)
            raise AuthenticationFailed(msg.authentication_failed) from e
        credentials = flow.credentials

        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        email = user_info['email']
        social_id = user_info['id']
        user = user_service.get_or_create_user_by_email(email)

        return self._get_or_create_soc_acc(
            social_id=social_id, social_name=self.social_name, user_id=user.id,
        )

    def _get_or_create_soc_acc(self,
                               social_id: str,
                               social_name: str,
                               user_id: UUID,
                               ) -> SocialAccount:
        """Получить SocialAccount, если нет, создать."""
        soc_acc = self.soc_acc_model.query.filter_by(social_id=social_id,
                                                     social_name=social_name,
                                                     ).first()
        if not soc_acc:
            soc_acc = self.soc_acc_model(social_id=social_id,
                                         social_name=social_name,
                                         user_id=user_id,
                                         )
            soc_acc.create()
        return soc_acc
