"""Роутеры для АПИ к сущности User."""

import uuid
from http import HTTPStatus
from auth.src.models import login_history

from flask import Blueprint
from flask_pydantic import validate

from api.v1.schemes.transform_schemes import (
    login_history_create_scheme_to_login_history_create_model,
)
from api.v1.schemes.login_histories import (
    LoginHistoryCreateScheme, LoginHistoryScheme, ListLoginHistoryScheme
)
from models import LoginHistory
from services.login_history import get_login_history_service

login_histories = Blueprint('login_histories', __name__)
login_history_service = get_login_history_service()


@login_histories.route('/signup', methods=['POST'])
@validate(on_success_status=HTTPStatus.CREATED)
def create_login_history(body: LoginHistoryCreateScheme) -> LoginHistoryScheme:
    """Создать историю логина пользователя."""
    login_history_model = login_history_create_scheme_to_login_history_create_model(
        login_history_scheme=body)

    login_history = login_history_service.register_user(
        login_history_in=login_history_model)

    login_history.save()
    return LoginHistoryScheme.parse_obj(login_history.as_dict)


@login_histories.route('/login_history/<login_history_id>/', methods=['GET'])
@validate()
def get_one_login_history(login_history_id: uuid.UUID) -> LoginHistory:
    """Подробная информация о пользователе."""
    login_history_obj = LoginHistory.get_or_404(id=login_history_id)
    return LoginHistory.parse_obj(login_history_obj.as_dict)


@login_histories.route('/login_histories/', methods=['GET'])
@validate()
def login_history_list(login_history_id: uuid.UUID) -> ListLoginHistoryScheme:
    """Список историй логинов пользователей."""
    login_history_obj = LoginHistory.get_or_404(id=login_history_id)
    login_histories = [
        LoginHistoryScheme.parse_obj(login_history.as_dict) for login_history in login_history_obj.roles
    ]
    return ListLoginHistoryScheme(login_histories=login_histories)
