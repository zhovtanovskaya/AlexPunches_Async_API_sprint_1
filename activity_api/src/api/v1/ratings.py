from fastapi import APIRouter, Depends, Request, Response, status

import src.api.v1.schemes.rating as schemes
from src.api.v1.schemes.transform_schemes import (
    transform_rating_model_to_scheme, transform_rating_scheme_to_model)
from src.auth.request import subscription_required
from src.services.ugc.models.custom_types import StrObjectId
from src.services.ugc.rating import RatingService, get_rating_service

router = APIRouter()


@router.post(
    '',
    dependencies=[Depends(subscription_required)],
    status_code=status.HTTP_201_CREATED,
)
async def create_rating(
    request: Request,
    rating: schemes.RatingCreateScheme,
    rating_service: RatingService = Depends(get_rating_service),
) -> schemes.RatingScheme:
    rating.user_id = request.state.user_id
    rating_model = transform_rating_scheme_to_model(rating)
    new_rating = await rating_service.create(obj=rating_model)
    return transform_rating_model_to_scheme(new_rating)


@router.delete('/{rating_id}', dependencies=[Depends(subscription_required)])
async def delete_rating(
    rating_id: StrObjectId,
    request: Request,
    rating_service: RatingService = Depends(get_rating_service),
) -> Response:
    await rating_service.delete(
        id=rating_id,
        filters={'user_id': str(request.state.user_id)},
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
