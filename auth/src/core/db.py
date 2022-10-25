from http import HTTPStatus

from core.exceptions import ResourceNotFoundError
from flask_sqlalchemy import BaseQuery, SQLAlchemy


class CustomBaseQuery(BaseQuery):
    def filter_by_or_404(self, **kwargs):
        rv = self.filter_by(**kwargs)
        if not rv.first():
            raise ResourceNotFoundError('Resource not found',
                                        status_code=HTTPStatus.NOT_FOUND)
        return rv


db = SQLAlchemy(query_class=CustomBaseQuery)
