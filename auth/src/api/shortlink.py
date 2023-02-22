"""Короткие ссылки подтверждения регисрации."""

from http import HTTPStatus

from flask import Blueprint, Response, redirect
from flask_pydantic import validate
from werkzeug.wrappers import Response as BaseResponse

from services.shortlink import ShortlinkService, get_shortlink_service
from utils import messages as msg

shortlink = Blueprint('shortlink', __name__)
shortlink_service: ShortlinkService = get_shortlink_service()


@shortlink.route('/<link_id>', methods=['GET'])
@validate()
def confirm_email(link_id: str) -> BaseResponse:
    """Редиректнуть короткую ссылку."""
    if redirect_url := shortlink_service.get_longlink_by_shortlink_id(link_id):
        return redirect(redirect_url, HTTPStatus.MOVED_PERMANENTLY)
    return Response(msg.shortlink_not_found, HTTPStatus.NOT_FOUND)
