"""Базовая SQLAlchemy-модель для БД."""

import uuid
from http import HTTPStatus
from typing import AbstractSet, Any, Mapping

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect

from core.db import db
from core.exceptions import BasicExceptionError, ResourceNotFoundError
from utils import messages as msg


class BaseModel(db.Model):
    """Модель, которая содержит некоторые общие базовые методы."""

    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)

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
            if _values[key] is not None:
                setattr(self, key, _values[key])

    @classmethod
    def get_or_404(cls, id: uuid.UUID):
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
