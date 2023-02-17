"""Точка входа в приложение."""
import asyncio

import sentry_sdk
import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse
from kafka.errors import KafkaConnectionError
from motor.motor_asyncio import AsyncIOMotorClient

from src import producer
from src.api.v1 import (activities, bookmarks, likes, ratings, reviews,
                        statistics)
from src.core.config import config
from src.core.context import request_id
from src.db import mongo

if config.activity_sentry_dsn:
    sentry_sdk.init(
        dsn=config.activity_sentry_dsn,
        traces_sample_rate=1.0,
    )
app = FastAPI(
    title=config.project_name,
    docs_url='/api/v1/activities/openapi',
    openapi_url='/api/v1/activities/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.middleware('http')
async def request_middleware(request: Request, call_next) -> Response:
    """Поймать заголовок X-Request-Id и придержать его в ContextVar."""
    request_id.set(request.headers.get('X-Request-Id', default=''))
    return await call_next(request)


@app.on_event('startup')
async def startup():
    """Запустить продюсера для Кафки."""
    loop = asyncio.get_event_loop()
    producer.producer = AIOKafkaProducer(
        loop=loop,
        client_id=config.project_name,
        bootstrap_servers=f'{config.event_store_host}:{config.event_store_port}', # noqa
    )
    try:
        await producer.producer.start()
    except KafkaConnectionError:
        pass
    mongo.mongo_db = AsyncIOMotorClient(
        config.mongo_url,
        serverSelectionTimeoutMS=5000,
        tls=bool(config.mongo_tls_ca_file),
        tlsCAFile=config.mongo_tls_ca_file,
    )[config.mongo_auth_src]


@app.on_event('shutdown')
async def shutdown():
    """Остановить продюсера для Кафки."""
    await producer.aioproducer.stop()


app.include_router(
    activities.router, prefix='/api/v1/activities', tags=['activity'],
)
app.include_router(
    likes.router, prefix='/api/v1/likes', tags=['likes'],
)
app.include_router(
    statistics.router, prefix='/api/v1/statistics', tags=['statistics'],
)
app.include_router(
    bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'],
)
app.include_router(
    ratings.router, prefix='/api/v1/ratings', tags=['ratings'],
)
app.include_router(
    reviews.router, prefix='/api/v1/reviews', tags=['reviews'],
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0', # noqa
        port=int(config.activity_api_port),
    )
