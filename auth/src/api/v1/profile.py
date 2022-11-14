"""Роутеры для АПИ к сущности User."""

import uuid
from http import HTTPStatus

from flask import Blueprint, Response
from flask_jwt_extended import get_jwt, jwt_required
from flask_pydantic import validate

import api.v1.schemes.transform_schemes as transform
import api.v1.schemes.users as user_schemes
from core.exceptions import ResourceNotAllowedError
from services.user import get_user_service
from utils import messages as msg

profile = Blueprint('profile', __name__)
user_service = get_user_service()


@profile.route('/profile', methods=['GET'])
@validate()
@jwt_required()
def get_one_user() -> user_schemes.UserScheme:
    """Подробная информация о пользователе."""
    if email := get_jwt().get('sub'):
        user_model = user_service.get_user_by_email(email=email)
        return transform.user_model_to_user_scheme(user_model=user_model)
    raise ResourceNotAllowedError(msg.not_allowed, HTTPStatus.FORBIDDEN)


@profile.route('/profile', methods=['PATCH'])
@validate()
@jwt_required()
def edit_user(body: user_schemes.UserEditScheme) -> user_schemes.UserScheme:
    """Редактировать информацию о пользователе."""
    user_model_new = transform.user_scheme_to_user_model(user_scheme=body)
    if email := get_jwt().get('sub'):
        user_id = user_service.get_user_by_email(email=email).id
        user_model_new.id = user_id
        updated_user = user_service.edit(user_in=user_model_new)
        return transform.user_model_to_user_scheme(user_model=updated_user)
    raise ResourceNotAllowedError(msg.not_allowed, HTTPStatus.FORBIDDEN)
