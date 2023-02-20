"""Сервис авторизации Google OAuth 2.0."""
from typing import Mapping, Type

import google_auth_oauthlib.flow
from googleapiclient.discovery import build

from core.config import config, logger
from db.db import db
from models.social_account import SocialAccount
from services.auth.exceptions import AuthenticationFailed
from services.social_auth.base_provider import BaseOAuth, SocUser
from services.user import get_user_service
from utils import messages as msg

user_service = get_user_service()


class GoogleOAuthProvider(BaseOAuth):
    """Управление авторизацией Гуловским OAuth."""

    soc_acc_model: Type[db.Model] = SocialAccount
    social_name: str = 'google_oauth'

    def get_oauth_url(self):
        """Получить url у Гугла, на который отправим юзера."""
        authorization_url, state = self._get_authorization_url()
        return authorization_url

    def auth(self,
             request_url: str,
             data: Mapping[str, str] | None = None,
             ) -> SocUser:
        """Пытаемся авторизоваться.

        :param request_url: url со всеми query параметрами в строке
        :param data: POST данные, в гугле их нет
        :return: SocUser
        """
        return self._auth_by_request_url(request_url=request_url)

    @staticmethod
    def _get_authorization_url() -> tuple[str, str]:
        """Получить урл Гугла, на котором юзер даст разрешения.

        В query параметрах будет список необходимых для нас разрешений,
        и другие полезные параметры, в том числе урл, куда юзер вернется
        с разрешениями. Подробнее:
        https://developers.google.com/identity/protocols/oauth2/web-server#python_1
        """
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=config.google_oauth,
            scopes=[
                'openid', 'https://www.googleapis.com/auth/userinfo.email'],
        )
        flow.redirect_uri = config.google_oauth_endpoint
        return flow.authorization_url(
            access_type='offline', include_granted_scopes='true',
        )

    @staticmethod
    def _auth_by_request_url(request_url: str) -> SocUser:
        """Авторизовать пользователя по колбеку от Гугла.

        Вместе в пользователем, гугл передает query-параметры, в которых всякое
        необходимое: код авторизации, разрешения, токены и т.д.
        Эти данные мы какбы конвертируем в credentials, которые уже позволят
        забрать у гугла инфу о пользователе и т.п.
        https://developers.google.com/identity/protocols/oauth2/web-server#handlingresponse
        """
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

        return SocUser(social_id=social_id, user_id=user.id)
