from uuid import UUID

from .base import ReactionService
from .models.user_content.ratings import Rating, RatingStats


class RatingService(ReactionService):

    user_content_type = Rating

    async def get_stats(self, movie_id: UUID) -> RatingStats:
        """Посчитать средний рейтинг и количество оценок фильма."""
        pipeline = [
            {
                '$match': {
                    'target_type': 'movie',
                    'type': 'rating',
                    'target_id': movie_id,
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
        return RatingStats(**results[0])
