from pydantic import BaseModel


class RatingStatisticScheme(BaseModel):
    total_ratings: int
    average_rating: float


class ReviewStatisticScheme(BaseModel):
    total_reviews: int
    positive_count: int
    negative_count: int
    neutral_count: int


class MovieStatisticScheme(BaseModel):
    ratings: RatingStatisticScheme
    reviews: ReviewStatisticScheme
