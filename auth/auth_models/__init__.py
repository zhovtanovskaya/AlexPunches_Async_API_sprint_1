import uuid
from http import HTTPStatus
from typing import AbstractSet, Any, Mapping

from core.config import config
from core.db import db
from core.exceptions import BasicExceptionError, ResourceNotFoundError
from flask_sqlalchemy import BaseQuery, Pagination
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from utils import messages as msg


class AdvanceModel(db.Model):
    __abstract__ = True
    page = config.paginator_start_page
    per_page = config.paginator_per_page

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)

    @classmethod
    def get_all(cls,
                paginator: bool = False,
                filter_by: Mapping[str, Any] | None = None,
                page: int = page,
                per_page: int = per_page,
                ) -> Pagination | BaseQuery:
        """
        Получить все объекты класса.
        :param filter_by: dict, добавить фильтров
        :param paginator: bool, если True, вернуть SqlAlchemy пагинатор
        :param page: номер страницы
        :param per_page: кол-во объектов на странице
        :return: Pagination | Query
        """
        query = db.session.query(cls).order_by(cls.id.desc())
        if filter_by:
            query = query.filter_by(**filter_by)
        if not paginator:
            return query.all()
        return query.paginate(
            page=page, per_page=per_page, error_out=False)

    @classmethod
    def get_or_404(cls, id: uuid.UUID):
        """Получить объект класса по ИД.
        Если нет -- отдать 404.
        """
        try:
            return db.session.query(cls).filter_by_or_404(
                id=id).first()
        except ResourceNotFoundError:
            db.session.rollback()
            raise ResourceNotFoundError(
                f"{cls.__name__} id={id} {msg.not_found_error}",
                HTTPStatus.NOT_FOUND
            )

    def create(self):
        """Добавить объект в БД."""
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise BasicExceptionError(
                f"Error: {e}", HTTPStatus.BAD_REQUEST) from e

    @staticmethod
    def save():
        """Закоммитить сессию."""
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise BasicExceptionError(
                f"{msg.not_saved}: {e}", HTTPStatus.INTERNAL_SERVER_ERROR
            ) from e

    def remove(self):
        """Удалить объект из БД."""
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise BasicExceptionError(
                f"{msg.not_deleted}: {e}", HTTPStatus.INTERNAL_SERVER_ERROR
            ) from e

    def edit_from_scheme(
        self,
        scheme: BaseModel,
        exclude: AbstractSet[str] | Mapping[int | str, Any] | None = None
    ) -> None:
        values_ = scheme.dict(exclude=exclude, exclude_unset=True)
        for key in values_:
            setattr(self, key, values_[key])

    @property
    def as_dict(self):
        props = {
            k: getattr(self, k) for (k, v) in vars(self.__class__).items()
            if type(v) is property
        }
        colums = {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }
        colums.update(**props)

        return colums


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
)
