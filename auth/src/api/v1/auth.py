"""API для аутентификации пользователя."""
from http import HTTPStatus

from flask import Blueprint, Response, jsonify
from flask_pydantic import validate

import services.auth.auth as services_auth
import services.jwt.token as services_jwt_token
from api.v1.schemes.auth import UserSigninScheme
from services.jwt.request import get_jwt, jwt_required

auth = Blueprint('auth', __name__)


@auth.route('/signin', methods=['POST'])
@validate()
def signin(body: UserSigninScheme):
    """Проверить, что пользователь существует и выдать пару JWT."""
    services_auth.authenticate(body.email, body.password)
    access_token, refresh_token = services_jwt_token.create_tokens(body.email)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth.route('/signout', methods=['POST'])
@jwt_required(refresh=True)
def signout():
    """Отозвать JWT доступа и обновления.

    Ожидает заголовок Authorization: Bearer <refresh_token>
    """
    jwt_payload = get_jwt()
    services_jwt_token.revoke_tokens(jwt_payload)
    return Response('', HTTPStatus.NO_CONTENT)


@auth.route('refresh/', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Получить новую пару JWT, и отозвать текущую пару JWT.

    Ожидает заголовок Authorization: Bearer <refresh_token>
    """
    jwt_payload = get_jwt()
    services_jwt_token.revoke_tokens(jwt_payload)
    access_token, refresh_token = services_jwt_token.create_tokens(
        jwt_payload['sub'],     # Содержит email пользователя.
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token)
