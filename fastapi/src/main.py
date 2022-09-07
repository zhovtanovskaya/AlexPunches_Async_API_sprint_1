import os
import sys

import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from api.v1 import films, genres, persons
from core.cache_middleware import RedisCacheMiddleware
from core.config import config
from db import elastic, redis

app = FastAPI(
    title=config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
            (config.redis_host, config.redis_port), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(
        hosts=[f'{config.elastic_host}:{config.elastic_port}']
    )


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])

my_middleware = RedisCacheMiddleware()
app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
