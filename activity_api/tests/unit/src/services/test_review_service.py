from src.services.models.user_content.reviews import Review, ReviewValue
from src.services.review import ReviewService
from tests.unit.src.base import ReactionTestCase


class TestReviewService(ReactionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.service = ReviewService(self.db)
        self.review = Review(
            user_id='af18023d-9c76-11ed-9485-7831c1bc31e4',
            target_id='6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4',
            value=ReviewValue.NEUTRAL,
            title='So-so movie.',
            text='Long and detailed explanations...',
        )

    async def test_get_all(self):
        new_review = await self.service.create(self.review)
        all_reviews = [r async for r in self.service.get_all()]
        self.assertEqual([new_review], all_reviews)
