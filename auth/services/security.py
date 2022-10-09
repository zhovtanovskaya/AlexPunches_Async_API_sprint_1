from functools import lru_cache
from typing import Any, Type

from core.db import db
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.registerable import register_user as security_register_user
from routers.v1.schemes.roles import RoleCreate
from routers.v1.schemes.users import UserCreate


class SecurityService:
    def __init__(self, user_model, role_model):
        self.security = SQLAlchemyUserDatastore(
            db=db, user_model=user_model, role_model=role_model
        )

    @staticmethod
    def register_user(scheme: UserCreate) -> db.Model:
        return security_register_user(**scheme.dict())

    def create_role(self, scheme: RoleCreate) -> db.Model:
        return self.security.create_role(**scheme.dict())

    def add_role_to_user(self, user: db.Model, role: db.Model) -> Any:
        return self.security.add_role_to_user(user=user, role=role)

    def remove_role_from_user(self, user: db.Model, role: db.Model) -> Any:
        return self.security.remove_role_from_user(user=user, role=role)

    def create_user(self, scheme: UserCreate) -> db.Model:
        return self.security.create_user(**scheme.dict())

    def add_roles(self, user: db.Model, roles: list[db.Model]) -> list[Any]:
        return [self.add_role_to_user(user=user, role=role) for role in roles]

    def remove_roles(self, user: db.Model, roles: list[db.Model]) -> list[Any]:
        return [
            self.remove_role_from_user(user=user, role=role) for role in roles]


@lru_cache()
def get_security_service(user_model: Type[db.Model],
                         role_model: Type[db.Model]
                         ) -> SecurityService:
    return SecurityService(user_model=user_model, role_model=role_model)
