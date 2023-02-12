"""Мидлваре для передачи X-Request-Id в контекст приложения."""
from fastapi import Request, Response

from core.context import request_id


class RequestIdMiddleware:
    async def __call__(self, request: Request, call_next) -> Response:
        request_id.set(request.headers.get('X-Request-Id', default=''))
        response = await call_next(request)
        return response
