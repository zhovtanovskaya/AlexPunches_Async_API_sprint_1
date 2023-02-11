"""Трансофмации из схем в модели и наоборот."""
from src.api.v1.schemes.bookmark import BookmarkBaseScheme, BookmarkScheme
from src.api.v1.schemes.like import LikeBaseScheme, LikeScheme
from src.api.v1.schemes.rating import RatingBaseScheme, RatingScheme
from src.api.v1.schemes.spawn_point import SpawnPointScheme
from src.api.v1.schemes.statistic import (RatingStatisticScheme,
                                          ReviewStatisticScheme)
from src.services.activity.models.spawn_point import SpawnPointModel
from src.services.ugc.models.bookmarks import Bookmark
from src.services.ugc.models.likes import Like
from src.services.ugc.models.ratings import Rating, RatingStats
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
        id=model.id,
        created_at=model.created_at,
        user_id=model.user_id,
        type=model.type,
        target_id=model.target_id,
        target_type=model.target_type,
    )


def transform_bookmark_scheme_to_model(scheme: BookmarkBaseScheme) -> Bookmark:
    """Трансформировать из схемы BookmarkBaseScheme в модель Bookmark."""
    return Bookmark(
        id=scheme.id,
        created_at=scheme.created_at,
        user_id=scheme.user_id,
        target_type=scheme.target_type,
        target_id=scheme.target_id,
    )


def transform_like_model_to_scheme(model: Like) -> LikeScheme:
    """Трансформировать из модели Like в схему LikeScheme."""
    return LikeScheme(
        id=model.id,
        created_at=model.created_at,
        user_id=model.user_id,
        type=model.type,
        target_id=model.target_id,
        target_type=model.target_type,
        value=model.value,
    )


def transform_like_scheme_to_model(scheme: LikeBaseScheme) -> Like:
    """Трансформировать из схемы LikeBaseScheme в модель Like."""
    return Like(
        id=scheme.id,
        created_at=scheme.created_at,
        user_id=scheme.user_id,
        target_id=scheme.target_id,
        target_type=scheme.target_type,
        value=scheme.value,
    )


def transform_rating_model_to_scheme(model: Rating) -> RatingScheme:
    """Трансформировать из модели Rating в схему RatingScheme."""
    return RatingScheme(
        id=model.id,
        created_at=model.created_at,
        user_id=model.user_id,
        type=model.type,
        target_id=model.target_id,
        target_type=model.target_type,
        value=model.value,
    )


def transform_rating_scheme_to_model(scheme: RatingBaseScheme) -> Rating:
    """Трансформировать из схемы RatingBaseScheme в модель Rating."""
    return Rating(
        id=scheme.id,
        created_at=scheme.created_at,
        user_id=scheme.user_id,
        target_id=scheme.target_id,
        target_type=scheme.target_type,
        value=scheme.value,
    )
