"""Роутеры для АПИ к сущности Role."""

from http import HTTPStatus

from flask import Blueprint, Response
from flask_pydantic import validate

import api.v1.schemes.roles as role_schemes
import api.v1.schemes.transform_schemes as transform
from services.jwt.request import admin_required
from services.role import get_role_service

roles = Blueprint('roles', __name__)
role_service = get_role_service()


@roles.route('/roles/', methods=['POST'])
@validate(on_success_status=HTTPStatus.CREATED)
@admin_required()
def create_role(
        body: role_schemes.RoleCreateScheme,
) -> role_schemes.RoleScheme:
    """Создать Роль."""
    role_model = transform.role_scheme_to_role_model(role_scheme=body)
    new_role_model = role_service.create_role(role=role_model)
    return transform.role_model_to_role_scheme(role_model=new_role_model)


@roles.route('/roles/', methods=['GET'])
@validate()
@admin_required()
def get_all_roles() -> role_schemes.ListRolesScheme:
    """Получить список Ролей."""
    _roles = role_service.get_roles_list()
    list_roles = [transform.role_model_to_role_scheme(role) for role in _roles]
    return role_schemes.ListRolesScheme(list_roles=list_roles)


@roles.route('/roles/<role_id>/', methods=['GET'])
@validate()
@admin_required()
def get_role_detail(role_id: int) -> role_schemes.RoleScheme:
    """Подробная информация о Роли."""
    role = role_service.get_role_by_id(id=role_id)
    return role_schemes.RoleScheme.from_orm(role)


@roles.route('/roles/<role_id>/', methods=['PATCH'])
@validate()
@admin_required()
def edit_role(role_id: int,
              body: role_schemes.RoleEditScheme,
              ) -> role_schemes.RoleScheme:
    """Редактировать Роль."""
    role_model = transform.role_scheme_to_role_model(role_scheme=body)
    role_model.id = role_id
    updated_role = role_service.edit_role(role=role_model)
    return transform.role_model_to_role_scheme(role_model=updated_role)


@roles.route('/roles/<role_id>/', methods=['DELETE'])
@validate()
@admin_required()
def remove_role(role_id: int) -> Response:
    """Удалить Роль."""
    role_service.delete_role(role_id=role_id)
    return Response('', HTTPStatus.NO_CONTENT)
