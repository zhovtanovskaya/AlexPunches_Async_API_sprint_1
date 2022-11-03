"""Сервис управления ролями в БД."""

from flask_sqlalchemy.extension import SQLAlchemy
from sqlalchemy.exc import IntegrityError

import models.role as orm_models
import services.models.role as services_models


class RoleService:
    """Сервис для доступа и редактирования ролей в БД."""

    def __init__(self, rdb: SQLAlchemy):
        """Проинициализировать подключение к БД."""
        self.rdb = rdb

    def create_role(
            self,
            role: services_models.Role,
            ) -> services_models.Role | None:
        """Создать роль в базе данных.

        Returns:
            Новый объект, представляющий запись в БД.  Или None
            в случае ошибки.
        """
        orm_role = orm_models.Role(
            name=role.name,
            description=role.description,
        )
        self.rdb.session.add(orm_role)
        try:
            self.rdb.session.commit()
        except IntegrityError:
            self.rdb.session.rollback()
            return None
        return services_models.Role.from_orm(orm_role)

    @staticmethod
    def get_roles_list() -> list[services_models.Role]:
        """Получить список всех ролей в БД."""
        roles = orm_models.Role.query.all()
        return [services_models.Role.from_orm(r) for r in roles]

    def delete_role(self, role_id: int):
        """Удалить роль из базы данных, если существует."""
        orm_role = orm_models.Role.query.get(role_id)
        if orm_role:
            self.rdb.session.delete(orm_role)
            self.rdb.session.commit()

    def update_role(
            self,
            role: services_models.Role,
            ) -> services_models.Role | None:
        """Обновить роль в базе данных.

        Returns:
            Новый объект, представляющий обновленную запись в БД.
            Или None, если записи с role.id в БД не существует.
        """
        if role.id is None:
            return
        orm_role = orm_models.Role.query.get(role.id)
        if orm_role:
            for field, value in role.dict().items():
                setattr(orm_role, field, value)
            self.rdb.session.add(orm_role)
            self.rdb.session.commit()
            return services_models.Role.from_orm(orm_role)
