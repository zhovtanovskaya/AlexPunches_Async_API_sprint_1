from functools import lru_cache
from typing import Type

from core.db import db
from flask_security.datastore import SQLAlchemyUserDatastore
from routers.v1.schemes.users import UserCreate


class SecurityService:
    def __init__(self, user_model, role_model):
        self.security = SQLAlchemyUserDatastore(
            db=db, user_model=user_model, role_model=role_model
        )

    def create_user(self, scheme: UserCreate) -> db.Model:
        return self.security.create_user(**scheme.dict())


@lru_cache()
def get_security_service(user_model: Type[db.Model],
                         role_model: Type[db.Model]
                         ) -> SecurityService:
    return SecurityService(user_model=user_model, role_model=role_model)
