from http import HTTPStatus

from flask import Blueprint, jsonify

exceptions = Blueprint('exceptions', __name__)


class BasicExceptionError(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error_message'] = self.message
        return rv


class ResourceNotFoundError(BasicExceptionError):
    pass


@exceptions.app_errorhandler(BasicExceptionError)
def exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@exceptions.app_errorhandler(ResourceNotFoundError)
def resource_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
