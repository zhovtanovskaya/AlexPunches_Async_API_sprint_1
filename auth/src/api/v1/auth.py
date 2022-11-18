"""API для аутентификации пользователя."""
from http import HTTPStatus

import flask
from flask import Blueprint, Response, jsonify
from flask_pydantic import validate

import services.auth.auth as services_auth
import services.jwt.token as services_jwt_token
from api.v1.schemes.auth import UserSigninScheme
from services.auth.google_oauth import GoogleOAuthService
from services.jwt.request import get_jwt, jwt_required

auth = Blueprint('auth', __name__)
google_oauth = GoogleOAuthService()


@auth.route('/signin', methods=['POST'])
@validate()
def signin(body: UserSigninScheme) -> Response:
    """Проверить, что пользователь существует и выдать пару JWT."""
    services_auth.authenticate(body.email, body.password)
    access_token, refresh_token = services_jwt_token.create_tokens(body.email)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth.route('/signout', methods=['POST'])
@jwt_required(refresh=True)
def signout() -> Response:
    """Отозвать JWT доступа и обновления.

    Ожидает заголовок Authorization: Bearer <refresh_token>
    """
    jwt_payload = get_jwt()
    services_jwt_token.revoke_tokens(jwt_payload)
    return Response('', HTTPStatus.NO_CONTENT)


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh() -> Response:
    """Получить новую пару JWT, и отозвать текущую пару JWT.

    Ожидает заголовок Authorization: Bearer <refresh_token>
    """
    jwt_payload = get_jwt()
    services_jwt_token.revoke_tokens(jwt_payload)
    access_token, refresh_token = services_jwt_token.create_tokens(
        jwt_payload['sub'],     # Содержит email пользователя.
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth.route('/google-signin', methods=['GET'])
@validate()
def google_signin() -> Response:
    """Получить ссылку на OAuth гугла."""
    authorization_url, state = google_oauth.get_authorization_url()
    return jsonify(authorization_url=authorization_url)


@auth.route('/google-auth', methods=['GET'])
@validate()
def google_auth():
    """Авторизовать."""
    request_url = flask.request.url
    soc_acc = google_oauth.auth_by_request_url(request_url=request_url)
    email = soc_acc.user.email

    # вернуть наши токены
    access_token, refresh_token = services_jwt_token.create_tokens(email)
    return jsonify(access_token=access_token, refresh_token=refresh_token)
