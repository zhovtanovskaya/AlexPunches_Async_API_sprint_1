"""Роутеры для аутенификаций и авторизаций."""
from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request

from services.auth import get_auth_service

auth = Blueprint('auth', __name__)
auth_service = get_auth_service()


@auth.route('/singin', methods=['GET', 'POST'])
def singin() -> Response:
    """Аутентифицировать пользователя по логину и паролю."""
    auth_data = request.authorization
    return auth_service.auth_user(auth_data=auth_data)


@auth.route('/signout', methods=['POST'])
def signout() -> Response:
    """Выйти."""
    if current_user_id := auth_service.get_current_user_id():
        auth_service.signout_user_by_id(user_id=current_user_id)
    return Response('', HTTPStatus.NO_CONTENT)


@auth.route('/refresh', methods=['POST'])
def refresh() -> tuple[Response, HTTPStatus]:
    """Выйти."""
    current_user_id = auth_service.get_current_user_id()
    tokens = auth_service.make_pair_tokens_by_user_id(user_id=current_user_id)
    return jsonify(tokens), HTTPStatus.OK
