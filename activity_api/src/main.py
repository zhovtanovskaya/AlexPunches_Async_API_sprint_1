"""Точка входа в приложение."""
import os
import sys

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


from producer import aioproducer

from api.v1 import activity
from core.config import config

app = FastAPI(
    title=config.project_name,
    docs_url='/api/v1/activity/openapi',
    openapi_url='/api/v1/activity/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    """Запустить продюсера для Кафки."""
    await aioproducer.start()


@app.on_event('shutdown')
async def shutdown():
    """Остановить продюсера для Кафки."""
    await aioproducer.stop()


app.include_router(
    activity.router, prefix='/api/v1/activity', tags=['activity'],
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0', # noqa
        port=int(config.api_port),
    )
