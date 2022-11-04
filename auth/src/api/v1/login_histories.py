"""Роутеры для АПИ к сущности User."""

import uuid
from http import HTTPStatus
from auth.src.models import login_history

from flask import Blueprint
from flask_pydantic import validate

from api.v1.schemes.login_histories import (
    LoginHistoryScheme, ListLoginHistoryScheme
)
from models import LoginHistory
from services.login_history import get_login_history_service

login_histories = Blueprint('login_histories', __name__)
login_history_service = get_login_history_service()


@login_histories.route('/login_histories/', methods=['GET'])
@validate()
def login_history_list() -> ListLoginHistoryScheme:
    """Список историй логинов пользователей."""
    login_history_obj = LoginHistory.objects.all()
    login_histories = [
        LoginHistoryScheme.parse_obj(
            login_history.as_dict) for login_history in login_history_obj
    ]
    return ListLoginHistoryScheme(login_histories=login_histories)
