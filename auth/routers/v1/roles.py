from http import HTTPStatus

from auth_models.role import Role
from flask import Blueprint, Response, jsonify
from flask_pydantic import validate
from routers.v1.schemes.roles import RoleCreate, RoleScheme
from utils import messages as msg

roles = Blueprint('roles', __name__,)


@roles.route('/roles', methods=['POST'])
@validate(on_success_status=HTTPStatus.CREATED)
def create_role(body: RoleCreate) -> RoleScheme:
    new_role = Role(name=body.name, description=body.description)
    new_role.create()
    return RoleScheme.parse_obj(new_role.as_dict)


@roles.route('/roles', methods=['GET'])
@validate(response_many=True)
def get_roles() -> list[RoleScheme]:
    _roles = Role.get_all()
    return [RoleScheme.parse_obj(role.as_dict) for role in _roles]


@roles.route('/roles/<role_id>', methods=['GET'])
@validate()
def get_one_role(role_id: int) -> RoleScheme | None:
    role = Role.get_or_404(id=role_id)
    return RoleScheme.parse_obj(role.as_dict)


@roles.route('/roles/<role_id>', methods=['PATCH'])
@validate()
def edit_role(role_id: int, body: RoleCreate) -> RoleScheme:
    role = Role.get_or_404(id=role_id)
    role.edit_from_scheme(scheme=body)
    role.save()
    return RoleScheme.parse_obj(role.as_dict)


@roles.route('/roles/<role_id>', methods=['DELETE'])
@validate()
def delete_role(role_id: int) -> tuple[Response, HTTPStatus]:
    role = Role.get_or_404(id=role_id)
    role.remove()
    return jsonify({'message': msg.removed_successfully}), HTTPStatus.OK
