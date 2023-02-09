from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt


class RatingStatisticScheme(BaseModel):
    total_ratings: NonNegativeInt = 0
    average_rating: NonNegativeFloat = 0


class ReviewStatisticScheme(BaseModel):
    total_reviews: NonNegativeInt = 0
    positive_count: NonNegativeInt = 0
    negative_count: NonNegativeInt = 0
    neutral_count: NonNegativeInt = 0


class MovieStatisticScheme(BaseModel):
    ratings: RatingStatisticScheme
    reviews: ReviewStatisticScheme
