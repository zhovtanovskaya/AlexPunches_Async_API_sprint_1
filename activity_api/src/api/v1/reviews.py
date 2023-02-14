import math
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import PositiveInt

import src.api.v1.schemes.review as schemes
from src.api.v1.schemes.transform_schemes import (
    transform_review_model_to_scheme, transform_review_scheme_to_model)
from src.auth.request import subscription_required
from src.services.ugc.models.custom_types import StrObjectId
from src.services.ugc.review import ReviewService, get_review_service

router = APIRouter()


@router.post(
    '',
    dependencies=[Depends(subscription_required)],
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    request: Request,
    review: schemes.ReviewCreateScheme,
    review_service: ReviewService = Depends(get_review_service),
) -> schemes.ReviewScheme:
    review.user_id = request.state.user_id
    review_model = transform_review_scheme_to_model(review)
    new_review = await review_service.create(obj=review_model)
    return transform_review_model_to_scheme(new_review)


@router.get('')
async def get_reviews(
    target_id: UUID,
    sort: str = '_id',
    page_number: PositiveInt = Query(default=1, alias='page[number]'),
    page_size: PositiveInt = Query(default=50, alias='page[size]'),
    review_service: ReviewService = Depends(get_review_service),
) -> schemes.ReviewPaginateScheme:
    reviews = review_service.get_all(
        sort=sort,
        filters={'target_id': str(target_id)},
        page_number=page_number,
        page_size=page_size,
    )
    review_stat = await review_service.get_stats(movie_id=target_id)
    return schemes.ReviewPaginateScheme(
        page={
            'total_pages': math.ceil(review_stat.total_reviews / page_size),
            'total_items': review_stat.total_reviews,
            'number': page_number,
            'size': page_size,
        },
        results=[
            transform_review_model_to_scheme(review)
            async for review in reviews
        ],
    )


@router.delete('/{review_id}', dependencies=[Depends(subscription_required)])
async def delete_review(
    review_id: StrObjectId,
    request: Request,
    review_service: ReviewService = Depends(get_review_service),
) -> Response:
    await review_service.delete(
        id=review_id,
        filters={'user_id': str(request.state.user_id)},
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
