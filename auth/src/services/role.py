"""Сервис управления ролями в БД."""
from functools import lru_cache
from typing import Type

import services.models.roles as service_models
from db.db import db
from models import Role, User


class RoleService:
    """Сервис для доступа и редактирования ролей в БД."""

    user_model: Type[db.Model] = User
    role_model: Type[db.Model] = Role

    def get_role_by_id(self, id: int) -> service_models.RoleModel:
        """Получить Роль."""
        role = self.role_model.get_or_404(id=id)
        return service_models.RoleModel.from_orm(role)

    def create_role(self, role: service_models.RoleCreateModel,
                    ) -> service_models.RoleModel:
        """Создать роль в базе данных.

        Returns:
            Новый объект, представляющий запись в БД.
        """
        new_role = self.role_model(**role.dict())
        new_role.create()
        return service_models.RoleModel.from_orm(new_role)

    def find_or_create_role(self, name: str) -> service_models.RoleModel:
        """Вернуть Роль по названию. Если несуществует -- создать и вернуть."""
        if (role := self._get_role_by_rolename(rolename=name)):
            return service_models.RoleModel.from_orm(role)
        return self.create_role(service_models.RoleCreateModel(name=name))

    def _get_role_by_rolename(self, rolename: str) -> Type[db.Model]:
        """Получить Роль по названию."""
        return self.role_model.query.filter(
            self.role_model.name == rolename,
        ).first()

    def get_roles_list(self) -> list[service_models.RoleModel]:
        """Получить список всех ролей в БД."""
        roles = self.role_model.query.all()
        return [service_models.RoleModel.from_orm(role) for role in roles]

    def delete_role(self, role_id: int) -> None:
        """Удалить роль из базы данных, если существует."""
        orm_role = self.role_model.get_or_404(id=role_id)
        orm_role.remove()

    def edit_role(self, role: service_models.RoleEditModel,
                  ) -> service_models.RoleModel | None:
        """Обновить роль в базе данных.

        Returns:
            Новый объект, представляющий обновленную запись в БД.
        """
        orm_role = self.role_model.get_or_404(role.id)
        orm_role.edit(scheme_in=role)
        orm_role.save()
        return service_models.RoleModel.from_orm(orm_role)


@lru_cache()
def get_role_service() -> RoleService:
    """Создать и/или вернуть синглтон RoleService."""
    return RoleService()
