from fastapi import APIRouter, Depends, Request, Response, status

import src.api.v1.schemes.like as schemes
from src.api.v1.schemes.transform_schemes import (
    transform_like_model_to_scheme, transform_like_scheme_to_model)
from src.auth.request import subscription_required
from src.services.ugc.like import LikeService, get_like_service
from src.services.ugc.models.custom_types import StrObjectId

router = APIRouter()


@router.post(
    '',
    dependencies=[Depends(subscription_required)],
    status_code=status.HTTP_201_CREATED,
)
async def create_like(
    request: Request,
    like: schemes.LikeCreateScheme,
    like_service: LikeService = Depends(get_like_service),
) -> schemes.LikeScheme:
    like.user_id = request.state.user_id
    like_model = transform_like_scheme_to_model(like)
    new_like = await like_service.create(obj=like_model)
    return transform_like_model_to_scheme(new_like)


@router.delete('/{like_id}', dependencies=[Depends(subscription_required)])
async def delete_like(
    like_id: StrObjectId,
    request: Request,
    like_service: LikeService = Depends(get_like_service),
) -> Response:
    await like_service.delete(
        id=like_id,
        filters={'user_id': str(request.state.user_id)},
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
