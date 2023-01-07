"""Эндпоинты обработки событий."""
from activity_service import ActivityService
from fastapi import APIRouter, Depends, status

from api.v1.schemes.spawn_point import SpawnPointScheme
from api.v1.schemes.transform_schemes import transform_point_scheme_to_model
from auth.request import subscription_required

router = APIRouter()


@router.post('/spawn-point',
             dependencies=[Depends(subscription_required)],
             status_code=status.HTTP_201_CREATED,
             )
async def send_activity(spawn_point: SpawnPointScheme,
                        activity_service: ActivityService = Depends(),
                        ) -> dict:
    """Отправить spawn-point в хранилище."""
    spawn_point_model = transform_point_scheme_to_model(scheme=spawn_point)
    await activity_service.send_spawn_point(point=spawn_point_model)
    return {'message': 'ok'}
