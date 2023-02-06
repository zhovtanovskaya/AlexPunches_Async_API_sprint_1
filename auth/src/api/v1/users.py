"""Роутеры для АПИ к сущности User."""

import uuid
from http import HTTPStatus

from flask import Blueprint, Response
from flask_pydantic import validate

import api.v1.schemes.transform_schemes as transform
import api.v1.schemes.user_roles as user_role_schemes
import api.v1.schemes.users as user_schemes
from services.jwt.request import admin_required
from services.user import get_user_service

users = Blueprint('users', __name__)
user_service = get_user_service()


@users.route('/signup', methods=['POST'])
@validate(on_success_status=HTTPStatus.CREATED)
def create_user(
        body: user_schemes.UserCreateScheme,
) -> user_schemes.UserScheme:
    """Создать пользователя."""
    user_model = transform.user_scheme_to_user_model(user_scheme=body)
    user = user_service.register_user(user_in=user_model)
    return transform.user_model_to_user_scheme(user_model=user)


@users.route('/users/<user_id>/', methods=['GET'])
@validate()
@admin_required()
def get_one_user(user_id: uuid.UUID) -> user_schemes.UserScheme:
    """Подробная информация о пользователе."""
    user = user_service.get_user_by_id(id=user_id)
    return transform.user_model_to_user_scheme(user_model=user)


@users.route('/users/<user_id>/', methods=['PATCH'])
@validate()
@admin_required()
def edit_user(user_id: uuid.UUID,
              body: user_schemes.UserEditScheme,
              ) -> user_schemes.UserScheme:
    """Редактировать информацию о пользователе."""
    user_model = transform.user_scheme_to_user_model(user_scheme=body)
    user_model.id = user_id
    updated_user = user_service.edit(user_in=user_model)
    return transform.user_model_to_user_scheme(user_model=updated_user)


@users.route('/users/<user_id>/roles/', methods=['POST'])
@validate(on_success_status=HTTPStatus.CREATED)
@admin_required()
def create_user_role(user_id: uuid.UUID,
                     body: user_role_schemes.UserRoleCreateScheme,
                     ) -> user_role_schemes.ListUserRolesScheme:
    """Добавить роль пользователю."""
    user_service.add_role_to_user_by_rolename(user_id=user_id,
                                              rolename=body.name,
                                              )
    user_roles = user_service.get_user_roles_by_user_id(user_id=user_id)
    user_roles_scheme = [transform.role_model_to_role_scheme(role_model=role) for role in user_roles]  # noqa
    return user_role_schemes.ListUserRolesScheme(user_roles=user_roles_scheme)


@users.route('/users/<user_id>/roles/', methods=['GET'])
@validate()
@admin_required()
def user_role_list(
        user_id: uuid.UUID,
) -> user_role_schemes.ListUserRolesScheme:
    """Список Ролей пользователя."""
    user_roles = user_service.get_user_roles_by_user_id(user_id=user_id)
    user_roles_scheme = [transform.role_model_to_role_scheme(role_model=role) for role in user_roles]  # noqa
    return user_role_schemes.ListUserRolesScheme(user_roles=user_roles_scheme)


@users.route('/users/<user_id>/roles/<role_id>/', methods=['DELETE'])
@validate()
@admin_required()
def remove_user_role(user_id: uuid.UUID,
                     role_id: int,
                     ) -> Response:
    """Удалить Роль у пользователя."""
    user_service.remove_role_from_user(user_id=user_id, role_id=role_id)
    return Response('', HTTPStatus.NO_CONTENT)
