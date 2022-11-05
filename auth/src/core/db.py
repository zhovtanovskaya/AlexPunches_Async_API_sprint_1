"""Подключить Алхимию."""

from http import HTTPStatus

from flask_sqlalchemy import BaseQuery, SQLAlchemy

from core.exceptions import ResourceNotFoundError
from utils import messages as msg


class CustomBaseQuery(BaseQuery):
    """Класс который расширяет BaseQuery полезными методами."""

    def filter_by_or_404(self, **kwargs):
        """Вернуть 404 в виде ResourceNotFoundError, если ответ от БД пуст."""
        rv = self.filter_by(**kwargs)
        if not rv.first():
            raise ResourceNotFoundError(msg.resource_not_found,
                                        status_code=HTTPStatus.NOT_FOUND)
        return rv


db = SQLAlchemy(query_class=CustomBaseQuery)
