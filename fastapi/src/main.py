import os
import sys
import time

import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Depends

from services.redis_client import RedisClient, get_redis_service

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from api.v1 import films, genres
from core import config
from db import elastic, redis


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    # dependencies=[Depends(get_redis_service)],
)


@app.on_event('startup')
async def startup():
    elastic.es = AsyncElasticsearch(
        hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}']
    )


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])


class MyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        redis.redis = aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
        self.redis = get_redis_service()
        pass

    async def dispatch(self,
                       request: Request,
                       call_next,
                       ):
        if request.method != 'GET':
            return await call_next(request)

        response = await self.redis.get_raw_by_key(key=request.url)
        pass
        # if not response:
        #     response = await call_next(request)
        #     await self.redis.put_rqw_to_cache(request.url, response)
        #
        # return response


app.add_middleware(MyMiddleware)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
