from functools import lru_cache
from typing import Type

from core.db import db
from routers.v1.schemes.roles import RoleCreate
from routers.v1.schemes.users import UserCreate, UserEdit
from services.security import get_security_service


class UserService:
    def __init__(self, user: db.Model, role_model: Type[db.Model]):
        self.user = user
        self.role_model = role_model
        self.security = get_security_service(
            user_model=self.user.__class__,
            role_model=role_model
        )

    def register_user(self, scheme: UserCreate) -> db.Model:
        return self.security.register_user(scheme=scheme)

    def create_role(self, scheme: RoleCreate) -> db.Model:
        return self.security.create_role(scheme=scheme)

    def add_role_to_user(self, role: db.Model):
        self.security.add_role_to_user(user=self.user, role=role)

    def edit_from_scheme(self, user: db.Model, scheme: UserEdit) -> db.Model:
        user.edit_from_scheme(scheme=scheme, exclude={'roles'})
        if scheme.roles is not None:
            roles = self._get_roles_by_list_str(scheme.roles)
            self._update_user_roles(new_roles=roles)
        return user

    def _get_roles_by_list_str(self, roles_str: list[str]) -> list[db.Model]:
        return db.session.query(self.role_model).filter(
            self.role_model.name.in_(roles_str)
            # self.role_model.id.in_(roles_str)
        ).all()

    def _update_user_roles(self, new_roles: list[db.Model]) -> list[db.Model]:
        if len(roles_for_del := list(set(self.user.roles) - set(new_roles))):
            self.security.remove_roles(user=self.user, roles=roles_for_del)

        if len(roles_for_add := list(set(new_roles) - set(self.user.roles))):
            self.security.add_roles(user=self.user, roles=roles_for_add)

        return self.user.roles


@lru_cache()
def get_user_service(user: db.Model,
                     role_model: Type[db.Model]
                     ) -> UserService:
    return UserService(user=user, role_model=role_model)
