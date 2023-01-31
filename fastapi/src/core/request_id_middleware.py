from fastapi import Request

from utils.request_id import request_id


class RequestIdMiddleware:
    async def __call__(self, request: Request, call_next):
        request_id.set(request.headers.get('X-Request-Id', default=''))
        response = await call_next(request)
        return response
