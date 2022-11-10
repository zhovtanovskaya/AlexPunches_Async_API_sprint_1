"""Импортировать сюда модели, чтобы потом импортировать их в одной строке."""

from .base import BaseModel
from .login_history import LoginHistory
from .role import Role
from .roles_users import roles_users
from .user import User

__all__ = ['BaseModel', 'Role', 'roles_users', 'User']
