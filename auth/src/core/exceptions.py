"""Набор кастомных исключений в виде Response jsonify."""

from http import HTTPStatus
from typing import Any, Mapping

from flask import Blueprint, Response, jsonify

exceptions = Blueprint('exceptions', __name__)


class BasicExceptionError(Exception):
    """Расширить возможности Exception.

    Чтобы сообщать отдавать клиету jsonify в API.
    """

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self,
                 message: str,
                 status_code: HTTPStatus | None = None,
                 payload: Mapping[str, Any] | None = None,
                 ) -> None:
        """Расширить инит дополнительными полезными данными."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Вернуть в виде дикта."""
        rv = dict(self.payload or ())
        rv['error_message'] = self.message
        return rv


class ResourceNotFoundError(BasicExceptionError):
    """Exception, когда что-то не нашлось."""

    pass


@exceptions.app_errorhandler(BasicExceptionError)
def exception(error: BasicExceptionError) -> Response:
    """Вернуть jsonify, чтобы для API хорошо."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@exceptions.app_errorhandler(ResourceNotFoundError)
def resource_not_found(error: ResourceNotFoundError) -> Response:
    """Вернуть jsonify, чтобы для API хорошо."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
