"""Роутеры для АПИ к сущности LoginHistory."""

import uuid

from flask import Blueprint
from flask_pydantic import validate

from api.v1.schemes.login_histories import (ListLoginHistoryScheme,
                                            LoginHistoryScheme)
from models import LoginHistory, User
from services.login_history import get_login_history_service

login_histories = Blueprint('login_histories', __name__)
login_history_service = get_login_history_service()
users = Blueprint('users', __name__)


@users.route('/users/<user_id>/singins/', methods=['GET'])
@validate()
def get_login_history(user_id: uuid.UUID) -> ListLoginHistoryScheme:
    """История входов текущего пользователя в систему."""
    user_obj = User.get_or_404(id=user_id)

    login_history = LoginHistory.filter_by(email=user_obj.email).all()
    list_schemes = [
        LoginHistoryScheme.from_orm(login) for login in login_history]

    return ListLoginHistoryScheme(login_histories=list_schemes)


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
