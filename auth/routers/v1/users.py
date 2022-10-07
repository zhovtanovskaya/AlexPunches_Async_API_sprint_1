import uuid
from http import HTTPStatus

from auth_models.user import User
from flask import Blueprint, Response, jsonify
from flask_pydantic import validate
from routers.v1.schemes.paginate import PaginationQuery, PaginationResponse
from routers.v1.schemes.users import UserCreate, UserEdit, UserScheme
from utils import messages as msg
from utils.service import paginator_to_response

users = Blueprint('users', __name__,)


@users.route('/users', methods=['POST'])
@validate(on_success_status=HTTPStatus.CREATED)
def create_user(body: UserCreate) -> UserScheme:
    """Создать пользователя."""
    user = User().create_user(scheme=body)
    return UserScheme.parse_obj(user.as_dict)


@users.route('/users', methods=['GET'])
@validate()
def get_users(query: PaginationQuery) -> PaginationResponse:
    paginator = User.get_all(paginator=True,
                             page=query.page, per_page=query.per_page)
    _users = [UserScheme.parse_obj(user.as_dict) for user in paginator.items]
    return paginator_to_response(paginator, results=_users)


@users.route('/users/<user_id>', methods=['GET'])
@validate()
def get_one_user(user_id: uuid.UUID) -> UserScheme:
    user = User.get_or_404(id=user_id)
    return UserScheme.parse_obj(user.as_dict)


@users.route('/users/<user_id>', methods=['PATCH'])
@validate()
def edit_user(user_id: uuid.UUID, body: UserEdit) -> UserScheme:
    user = User.get_or_404(id=user_id)
    user.edit_from_scheme(body_scheme=body)
    user.save()
    return UserScheme.parse_obj(user.as_dict)


@users.route('/users/<user_id>', methods=['DELETE'])
@validate()
def delete_user(user_id: uuid.UUID) -> tuple[Response, HTTPStatus]:
    user = User.get_or_404(id=user_id)
    user.remove()
    return jsonify({'message': msg.removed_successfully}), HTTPStatus.OK
