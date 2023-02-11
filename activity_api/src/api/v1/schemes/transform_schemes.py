"""Трансофмации из схем в модели и наоборот."""
from src.api.v1.schemes.bookmark import BookmarkScheme
from src.api.v1.schemes.spawn_point import SpawnPointScheme
from src.api.v1.schemes.statistic import (RatingStatisticScheme,
                                          ReviewStatisticScheme)
from src.services.activity.models.spawn_point import SpawnPointModel
from src.services.ugc.models.bookmarks import Bookmark
from src.services.ugc.models.ratings import RatingStats
from src.services.ugc.models.reviews import ReviewStats


def transform_point_scheme_to_model(
    scheme: SpawnPointScheme,
) -> SpawnPointModel:
    """Трансформировать из схемы в модель."""
    return SpawnPointModel(
        film_id=scheme.film_id,
        time=scheme.time,
    )


def transform_reviewstats_model_to_scheme(
    model: ReviewStats,
) -> ReviewStatisticScheme:
    """Трансформировать из модели ReviewStats в схему ReviewStatisticScheme."""
    return ReviewStatisticScheme(
        total_reviews=model.total_reviews,
        positive_count=model.positive_count,
        negative_count=model.negative_count,
        neutral_count=model.neutral_count,
    )


def transform_ratingstats_model_to_scheme(
    model: RatingStats,
) -> RatingStatisticScheme:
    """Трансформировать из модели RatingStats в схему RatingStatisticScheme."""
    return RatingStatisticScheme(
        total_ratings=model.total_ratings,
        average_rating=model.average_rating,
    )


def transform_bookmark_model_to_scheme(model: Bookmark) -> BookmarkScheme:
    """Трансформировать из модели Bookmark в схему BookmarkScheme."""
    return BookmarkScheme(
        id=str(model.id),
        created_at=model.created_at,
        user_id=model.user_id,
        type=model.type,
        target_id=model.target_id,
        target_type=model.target_type,
    )
