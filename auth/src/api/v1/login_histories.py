"""Роутеры для АПИ к сущности LoginHistory."""

import uuid

from flask import Blueprint
from flask_jwt_extended import get_jwt, jwt_required
from flask_pydantic import validate

from api.v1.schemes.login_histories import (ListLoginHistoryScheme,
                                            LoginHistoryScheme)
from core.db import db
from models import LoginHistory, User

login_histories = Blueprint('login_histories', __name__)


@login_histories.route('/users/<user_id>/singins/', methods=['GET'])
@validate()
def get_login_history(user_id: uuid.UUID) -> ListLoginHistoryScheme:
    """История входов пользователя в систему."""
    user_obj = User.get_or_404(id=user_id)
    login_history = db.session.query(LoginHistory).filter_by(
        email=user_obj.email).all()
    list_schemes = [
        LoginHistoryScheme.from_orm(login) for login in login_history
    ]
    return ListLoginHistoryScheme(login_histories=list_schemes)


@login_histories.route('/profile/singins/', methods=['GET'])
@validate()
@jwt_required()
def get_profile_history() -> ListLoginHistoryScheme:
    """История входов авторизованного пользователя в систему."""
    email = get_jwt().get('sub')
    # TODO продолжить копипастой предыдущего енпоинта
