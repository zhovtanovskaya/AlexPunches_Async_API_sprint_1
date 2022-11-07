"""Роутеры для АПИ к сущности User."""

import uuid
from http import HTTPStatus

from flask import Blueprint, Response
from flask_pydantic import validate

from api.v1.schemes.transform_schemes import (
    user_create_scheme_to_user_create_model,
    user_edit_scheme_to_user_edit_model)
from api.v1.schemes.user_roles import (ListUserRolesScheme, RoleScheme,
                                       UserRoleCreateScheme)
from api.v1.schemes.users import UserCreateScheme, UserEditScheme, UserScheme
from core.exceptions import ResourceNotFoundError
from models import Role, User
from services.user import get_user_service
from services.user_role import get_user_role_service
from utils import messages as msg

users = Blueprint('users', __name__)
user_service = get_user_service()
user_role_service = get_user_role_service()


@users.route('/signup', methods=['POST'])
@validate(on_success_status=HTTPStatus.CREATED)
def create_user(body: UserCreateScheme) -> UserScheme:
    """Создать пользователя."""
    user_model = user_create_scheme_to_user_create_model(user_scheme=body)
    user = user_service.register_user(user_in=user_model)
    user.save()
    return UserScheme.parse_obj(user.as_dict)


@users.route('/users/<user_id>/', methods=['GET'])
@validate()
def get_one_user(user_id: uuid.UUID) -> UserScheme:
    """Подробная информация о пользователе."""
    user_obj = User.get_or_404(id=user_id)
    return UserScheme.parse_obj(user_obj.as_dict)


@users.route('/users/<user_id>/', methods=['PATCH'])
@validate()
def edit_user(user_id: uuid.UUID, body: UserEditScheme) -> UserScheme:
    """Редактировать информацию о пользователе."""
    user_obj = User.get_or_404(id=user_id)
    user_model = user_edit_scheme_to_user_edit_model(user_scheme=body)
    user_service.edit_user(user_obj=user_obj, user_in=user_model)
    user_obj.save()
    return UserScheme.parse_obj(user_obj.as_dict)


@users.route('/users/<user_id>/roles/', methods=['POST'])
@validate(on_success_status=HTTPStatus.CREATED)
def create_user_role(user_id: uuid.UUID,
                     body: UserRoleCreateScheme,
                     ) -> ListUserRolesScheme:
    """Добавить роль пользователю."""
    user_obj = User.get_or_404(id=user_id)
    user_role_service.create_user_role_by_rolename(
        user=user_obj, rolename=body.name,
    )
    user_obj.save()
    user_roles = [
        RoleScheme.parse_obj(role.as_dict) for role in user_obj.roles
    ]
    return ListUserRolesScheme(user_roles=user_roles)


@users.route('/users/<user_id>/roles/', methods=['GET'])
@validate()
def user_role_list(user_id: uuid.UUID) -> ListUserRolesScheme:
    """Список Ролей пользователя."""
    user_obj = User.get_or_404(id=user_id)
    user_roles = [
        RoleScheme.parse_obj(role.as_dict) for role in user_obj.roles
    ]
    return ListUserRolesScheme(user_roles=user_roles)


@users.route('/users/<user_id>/roles/<role_id>/', methods=['DELETE'])
@validate()
def remove_user_role(user_id: uuid.UUID,
                     role_id: int,
                     ) -> tuple[Response, HTTPStatus]:
    """Удалить Роль у пользователя."""
    user_obj = User.get_or_404(id=user_id)
    role_obj = Role.get_or_404(id=role_id)
    if user_role_service.remove_user_role(user_obj=user_obj,
                                          role_obj=role_obj,
                                          ):
        user_obj.save()
    else:
        raise ResourceNotFoundError(msg.not_found_user_role_error)
    return Response(), HTTPStatus.NO_CONTENT