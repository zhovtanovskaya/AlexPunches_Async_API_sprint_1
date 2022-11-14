"""Роутеры для АПИ к сущности LoginHistory."""

import uuid

from flask import Blueprint
from flask_jwt_extended import get_jwt, jwt_required
from flask_pydantic import validate

from api.v1.schemes.login_histories import (ListLoginHistoryScheme,
                                            LoginHistoryScheme)
from api.v1.schemes.pagination import Page
from core.db import db
from models import LoginHistory, User
from services.jwt.request import admin_required

login_histories = Blueprint('login_histories', __name__)


@login_histories.route('/users/<user_id>/singins', methods=['GET'])
@validate()
@admin_required()
def get_login_history(
        user_id: uuid.UUID,
        query: Page,
        ) -> ListLoginHistoryScheme:
    """Страница истории входов пользователя в систему."""
    user_obj = User.get_or_404(id=user_id)
    login_history = db.session.query(LoginHistory).filter_by(
        email=user_obj.email,
    ).paginate(
        page=query.page_number,
        per_page=query.per_page,
        error_out=False,
        count=True,
    )
    list_schemes = [LoginHistoryScheme.from_orm(l) for l in login_history]
    return ListLoginHistoryScheme(
        login_histories=list_schemes,
        page_number=login_history.page,
        per_page=login_history.per_page,
        total_items=login_history.total,
    )


@login_histories.route('/profile/singins', methods=['GET'])
@validate()
@jwt_required()
def get_profile_history(query: Page) -> ListLoginHistoryScheme:
    """История входов авторизованного пользователя в систему."""
    email = get_jwt().get('sub')
    login_history = db.session.query(LoginHistory).filter_by(
        email=email,
    ).order_by(LoginHistory.date_login.desc()).paginate(
        page=query.page_number,
        per_page=query.per_page,
        error_out=False,
        count=True,
    )
    list_schemes = [LoginHistoryScheme.from_orm(l) for l in login_history]
    return ListLoginHistoryScheme(
        login_histories=list_schemes,
        page_number=login_history.page,
        per_page=login_history.per_page,
        total_items=login_history.total,
    )
