"""API для аутентификации пользователя."""

from flask import Blueprint, jsonify
from flask_pydantic import validate

import services.jwt.token as services_jwt_token
from api.v1.schemes.auth import UserSigninScheme

auth = Blueprint('auth', __name__)


@auth.route('/signin', methods=['POST'])
@validate()
def signin(body: UserSigninScheme):
    """Залогинить пользователя."""
    access_token, refresh_token = services_jwt_token.create_tokens(body.email)
    return jsonify(access_token=access_token, refresh_token=refresh_token)
