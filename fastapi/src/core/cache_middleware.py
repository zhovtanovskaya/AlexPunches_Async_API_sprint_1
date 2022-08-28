import pickle

from core import config
from db import redis
from models.json_response import CacheResponseScheme
from starlette.responses import StreamingResponse

from fastapi import Request


class RedisCacheMiddleware:
    async def __call__(self, request: Request, call_next) -> StreamingResponse:
        def strim_content(content_: list):
            yield from content_

        self.redis = await redis.get_redis()

        if (request.method != 'GET' or
                request.headers.get('X-Not-Cache') == 'True'):
            return await call_next(request)

        cache = await self.redis.get(key=str(request.url))
        if cache is None:
            response = await call_next(request)

            if response.background is not None:
                return response

            content = [i async for i in response.body_iterator]

            cache_obj = CacheResponseScheme(
                content=content,
                status_code=response.status_code,
                headers=response.headers,
                media_type=response.media_type,
            )
            await self.redis.set(str(request.url), pickle.dumps(cache_obj),
                                 expire=config.REDIS_CACHE_EXPIRE_IN_SECONDS)
        else:
            cache_obj = pickle.loads(cache)
            cache_obj.headers['X-From-Redis-Cache'] = 'True'

        return StreamingResponse(
                content=strim_content(cache_obj.content),
                status_code=cache_obj.status_code,
                headers=cache_obj.headers,
                media_type=cache_obj.media_type,
            )
