"""Эндпоинты запросов статистики."""
from uuid import UUID

from fastapi import APIRouter, Depends

from api.v1.schemes.statistic import MovieStatisticScheme
from services.rating import RatingService, get_ratind_service
from services.review import ReviewService, get_review_service

router = APIRouter()


@router.get('/movies/{movie_id}')
async def get_movie_stats(
    movie_id: UUID,
    rating_service: RatingService = Depends(get_ratind_service),
    review_service: ReviewService = Depends(get_review_service),
) -> MovieStatisticScheme:
    ratings = await rating_service.get_stats(movie_id)
    reviews = await review_service.get_stats(movie_id)
    # TODO будут какие-то трансформации?
    return MovieStatisticScheme(ratings=ratings, reviews=reviews)
