"""Эндпоинты обработки событий."""
from activity_service import ActivityService
from fastapi import APIRouter, Depends

from models import ActivityModel

router = APIRouter()


@router.post('/', status_code=201)
async def send_activity(activity: ActivityModel,
                        activity_service: ActivityService = Depends(),
                        ) -> dict:
    """Отправить событие в хранилище."""
    await activity_service.send(activity=activity)
    return {'oops': 'ok'}
