"""Базовая SQLAlchemy-модель для БД."""

from http import HTTPStatus
from typing import AbstractSet, Any, Mapping

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.inspection import inspect

from core.config import config
from core.db import db
from core.exceptions import BasicExceptionError, ResourceNotFoundError
from utils import messages as msg


class BaseModel(db.Model):
    """Модель, которая содержит некоторые общие базовые методы."""

    __abstract__ = True
    page = config.paginator_start_page
    per_page = config.paginator_per_page

    @classmethod
    def get_all(cls,
                paginator=False,
                filter_by=None,
                page=page,
                per_page=per_page,
                ):
        """Получить все объекты класса.

        :param filter_by: dict, добавить фильтров
        :param paginator: bool, если True, вернуть SqlAlchemy пагинатор
        :param page: номер страницы
        :param per_page: кол-во объектов на странице
        :return: SqlAlchemy.[paginator | query]
        """
        try:
            query = db.session.query(cls).order_by(cls.id.desc())
            if filter_by:
                query = query.filter_by(**filter_by)
            if not paginator:
                return query.all()
            return query.paginate(
                page, per_page, False)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise BasicExceptionError(
                f'{cls.__name__} {msg.not_found_error}',
                HTTPStatus.BAD_REQUEST,
            ) from e

    def create(self):
        """Добавить объект в БД."""
        db.session.add(self)
        try:
            self.save()
        except BasicExceptionError as e:
            raise BasicExceptionError(msg.not_created,
                                      HTTPStatus.INTERNAL_SERVER_ERROR,
                                      ) from e

    @classmethod
    def save(cls):
        """Закоммитить сессию."""
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise BasicExceptionError(
                f'{cls.__name__} {msg.not_saved}: {e}',
                HTTPStatus.INTERNAL_SERVER_ERROR,
            ) from e

    def edit(self,
             scheme_in: PydanticBaseModel,
             exclude: AbstractSet[str] | Mapping[int | str, Any] | None = None,
             ) -> None:
        """Редактировать объект."""
        _values = scheme_in.dict(exclude=exclude, exclude_unset=True)
        for key in _values:
            setattr(self, key, _values[key])

    def remove(self):
        """Удалить объект из БД."""
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise BasicExceptionError(
                f'{msg.not_removed}: {e}', HTTPStatus.INTERNAL_SERVER_ERROR,
            ) from e

    @classmethod
    def get_or_404(cls, id: Any):
        """Получить объект класса по ИД. Если нет -- отдать 404."""
        try:
            return db.session.query(cls).filter_by_or_404(
                id=id).first()
        except ResourceNotFoundError:
            db.session.rollback()
            raise ResourceNotFoundError(
                f'{cls.__name__} {msg.not_found_error}, id={id}',
                HTTPStatus.NOT_FOUND,
            )

    @property
    def as_dict(self):
        """Представить объект в виде словаря. Атребуты и проперти."""
        props = {
            k: getattr(self, k) for (k, v) in vars(self.__class__).items()
            if type(v) is property
        }
        attrs = {
            k: getattr(self, k) for (k, v)
            in inspect(self.__class__).attrs.items()
        }
        attrs.update(**props)
        return attrs
