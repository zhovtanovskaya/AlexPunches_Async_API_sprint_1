from src.services.models.user_content.ratings import Rating
from src.services.rating import RatingService
from tests.unit.src.base import ReactionTestCase


class TestRatingService(ReactionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.service = RatingService(self.db)
        rating = Rating(
            user_id='af18023d-9c76-11ed-9485-7831c1bc31e4',
            target_id='6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4',
            value=10,
        )
        self.new_rating = await self.service.create(rating)

    async def test_get_stats(self):
        stats = await self.service.get_stats(self.new_rating.target_id)
        self.assertEqual({'total_ratings': 1, 'average_rating': 10}, stats)
