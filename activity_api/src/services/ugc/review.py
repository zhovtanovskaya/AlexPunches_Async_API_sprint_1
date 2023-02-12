from functools import lru_cache
from typing import Type
from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.mongo import get_mongo_db
from src.services.ugc.base import ReactionService
from src.services.ugc.models.reviews import Review, ReviewStats, ReviewValue


class ReviewService(ReactionService):

    user_content_type = Type[Review]

    async def get_stats(self, movie_id: UUID) -> ReviewStats:
        """Получить число разных ревью на фильм."""
        pipeline = [
            {
                '$match': {
                    'target_type': 'movie',
                    'type': 'review',
                    'target_id': str(movie_id),
                },
            },
            {'$group': {'_id': '$value', 'count': {'$count': {}}}},
        ]
        cursor = self.collection.aggregate(pipeline)
        stats = {d['_id']: d['count'] async for d in cursor}
        return ReviewStats(
            positive_count=stats.get(ReviewValue.POSITIVE, 0),
            neutral_count=stats.get(ReviewValue.NEUTRAL, 0),
            negative_count=stats.get(ReviewValue.NEGATIVE, 0),
            total_reviews=sum(stats.values()),
        )


@lru_cache()
def get_review_service(
    mongo: AsyncIOMotorDatabase = Depends(get_mongo_db)
) -> ReviewService:
    return ReviewService(mongo)
