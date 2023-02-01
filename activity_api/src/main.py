"""Точка входа в приложение."""
import asyncio
import os
import sys

import sentry_sdk
import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import producer

from api.v1 import activities
from core.config import config

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


@app.on_event('startup')
async def startup():
    """Запустить продюсера для Кафки."""
    loop = asyncio.get_event_loop()
    producer.aioproducer = AIOKafkaProducer(
        loop=loop,
        client_id=config.project_name,
        bootstrap_servers=f'{config.event_store_host}:{config.event_store_port}', # noqa
    )
    await producer.aioproducer.start()


@app.on_event('shutdown')
async def shutdown():
    """Остановить продюсера для Кафки."""
    await producer.aioproducer.stop()


app.include_router(
    activities.router, prefix='/api/v1/activities', tags=['activity'],
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0', # noqa
        port=int(config.activity_api_port),
    )
