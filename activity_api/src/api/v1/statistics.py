"""Эндпоинты запросов статистики."""
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.v1.schemes.statistic import MovieStatisticScheme
from src.api.v1.schemes.transform_schemes import (
    transform_ratingstats_model_to_scheme,
    transform_reviewstats_model_to_scheme)
from src.services.ugc.rating import RatingService, get_ratind_service
from src.services.ugc.review import ReviewService, get_review_service

router = APIRouter()


@router.get('/movies/{movie_id}')
async def get_movie_stats(
    movie_id: UUID,
    rating_service: RatingService = Depends(get_ratind_service),
    review_service: ReviewService = Depends(get_review_service),
) -> MovieStatisticScheme:
    ratings = await rating_service.get_stats(movie_id)
    reviews = await review_service.get_stats(movie_id)
    reviews = transform_reviewstats_model_to_scheme(reviews)
    ratings = transform_ratingstats_model_to_scheme(ratings)
    # TODO будут какие-то трансформации?
    return MovieStatisticScheme(ratings=ratings, reviews=reviews)
