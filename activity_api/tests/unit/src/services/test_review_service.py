from src.services.ugc.models.user_content.reviews import Review, ReviewValue
from src.services.ugc.review import ReviewService
from tests.unit.src.base import ReactionTestCase


class TestReviewService(ReactionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.service = ReviewService(self.db)
        review = Review(
            user_id='af18023d-9c76-11ed-9485-7831c1bc31e4',
            target_id='6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4',
            value=ReviewValue.NEUTRAL,
            title='So-so movie.',
            text='Explanations...',
        )
        self.new_review = await self.service.create(review)

    async def test_get_all(self):
        all_reviews = [r async for r in self.service.get_all()]
        self.assertEqual([self.new_review], all_reviews)

    async def test_get_all_pagination(self):
        all_reviews = [r async for r in self.service.get_all(2, 1)]
        self.assertEqual([], all_reviews)

    async def test_get_stats(self):
        stats = await self.service.get_stats(self.new_review.target_id)
        expected = {
            'total_reviews': 1,
            'positive_count': 0,
            'neutral_count': 1,
            'negative_count': 0,
        }
        self.assertEqual(expected, stats.dict())
