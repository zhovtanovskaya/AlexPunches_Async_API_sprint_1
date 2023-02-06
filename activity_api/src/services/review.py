from typing import AsyncIterable
from uuid import UUID

from .base import ReactionService
from .models.user_content.reviews import Review, ReviewStats, ReviewValue


class ReviewService(ReactionService):

    user_content_type = Review

    async def get_all(self) -> AsyncIterable:
        result = self.collection.find({'type':  'review'})
        async for doc in result:
            yield self.to_obj(doc)

    async def get_stats(self, movie_id: UUID) -> ReviewStats:
        """Получить число разных ревью на фильм."""
        pipeline = [
            {
                '$match': {
                    'target_type': 'movie',
                    'type': 'review',
                    'target_id': movie_id,
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
