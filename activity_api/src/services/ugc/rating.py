from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.mongo import get_mongo_db
from src.services.ugc.base import ReactionService
from src.services.ugc.models.ratings import Rating, RatingStats


class RatingService(ReactionService):

    user_content_type = Rating

    async def get_stats(self, movie_id: UUID) -> RatingStats:
        """Посчитать средний рейтинг и количество оценок фильма."""
        pipeline = [
            {
                '$match': {
                    'target_type': 'movie',
                    'type': 'rating',
                    'target_id': str(movie_id),
                },
            },
            {
                '$group': {
                    '_id': '$target_id',
                    'average_rating': {'$avg': '$value'},
                    'total_ratings': {'$count': {}},
                },
            },
        ]
        results = await self.collection.aggregate(pipeline).to_list(1)
        if len(results) == 0:
            return RatingStats()
        return RatingStats(**results[0])


@lru_cache()
def get_ratind_service(
    mongo: AsyncIOMotorDatabase = Depends(get_mongo_db)
) -> RatingService:
    return RatingService(mongo)
