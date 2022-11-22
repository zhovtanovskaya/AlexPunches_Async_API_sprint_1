"""API для аутентификации пользователя."""
from http import HTTPStatus

import flask
from flask import Blueprint, Response, jsonify
from flask_pydantic import validate

import services.auth.auth as services_auth
import services.jwt.token as services_jwt_token
import services.social_auth as social_auth_service
from api.v1.schemes.auth import UserSigninScheme
from services.jwt.request import get_jwt, jwt_required

auth = Blueprint('auth', __name__)


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


@auth.route('/social-signin/<service_name>', methods=['GET'])
def social_signin(service_name: str) -> Response:
    """Получить ссылку на OAuth сервис."""
    oauth_service = social_auth_service.get_oauth_service(service=service_name)
    return jsonify(authorization_url=oauth_service.get_oauth_url())


@auth.route('/social-auth/<service_name>', methods=['GET', 'POST'])
def social_auth(service_name: str) -> Response:
    """Авторизовать пользователя, вернувшегося от гугла с разрешениями."""
    oauth_service = social_auth_service.get_oauth_service(service=service_name)
    request_url = flask.request.url
    request_data = flask.request.form
    soc_acc = oauth_service.auth(request_url=request_url, data=request_data)
    email = soc_acc.user.email

    # вернуть наши токены
    access_token, refresh_token = services_jwt_token.create_tokens(email)
    return jsonify(access_token=access_token, refresh_token=refresh_token)
