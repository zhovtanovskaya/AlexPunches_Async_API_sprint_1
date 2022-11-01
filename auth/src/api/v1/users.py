import uuid
from http import HTTPStatus

from flask import Blueprint, Response, jsonify
from flask_pydantic import validate

from api.v1.schemes.user_roles import ListUserRolesScheme, RoleScheme
from api.v1.schemes.users import UserScheme
from models import Role, User
from models.schemes.user_roles import UserRoleCreateScheme
from models.schemes.users import UserCreateScheme, UserEditScheme
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
    user = user_service.register_user(user_in=body)
    user.save()
    return UserScheme.parse_obj(user.as_dict)


@users.route('/users/<user_id>/', methods=['GET'])
@validate()
def get_one_user(user_id: uuid.UUID) -> UserScheme:
    """Подробная информация о пользователе."""
    user = User.get_or_404(id=user_id)
    return UserScheme.parse_obj(user.as_dict)


@users.route('/users/<user_id>/', methods=['PATCH'])
@validate()
def edit_user(user_id: uuid.UUID, body: UserEditScheme) -> UserScheme:
    """Редактировать информацию о пользователе."""
    user = User.get_or_404(id=user_id)
    user_service.edit_user(user_obj=user, user_in=body)
    user.save()
    return UserScheme.parse_obj(user.as_dict)


@users.route('/users/<user_id>/roles/', methods=['POST'])
@validate(on_success_status=HTTPStatus.CREATED)
def create_user_role(user_id: uuid.UUID,
                     body: UserRoleCreateScheme,
                     ) -> ListUserRolesScheme:
    """Добавить роль пользователю."""
    user = User.get_or_404(id=user_id)
    user_role_service.create_user_role_by_rolename(
        user=user, rolename=body.name,
    )
    user.save()
    user_roles = [RoleScheme.parse_obj(role.as_dict) for role in user.roles]
    return ListUserRolesScheme(user_roles=user_roles)


@users.route('/users/<user_id>/roles/', methods=['GET'])
@validate()
def user_role_list(user_id: uuid.UUID) -> ListUserRolesScheme:
    """Список Ролей пользователя."""
    user = User.get_or_404(id=user_id)
    user_roles = [RoleScheme.parse_obj(role.as_dict) for role in user.roles]
    return ListUserRolesScheme(user_roles=user_roles)


@users.route('/users/<user_id>/roles/<role_id>/', methods=['DELETE'])
@validate()
def remove_user_role(user_id: uuid.UUID,
                     role_id: int,
                     ) -> tuple[Response, HTTPStatus]:
    """Удалить Роль у пользователя."""
    user = User.get_or_404(id=user_id)
    role = Role.get_or_404(id=role_id)
    user_role_service.remove_user_role(user=user, role=role)
    user.save()
    return jsonify({'message': msg.removed_successfully}), HTTPStatus.OK
