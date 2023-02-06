import unittest

from motor.motor_asyncio import AsyncIOMotorClient

from src.services.models.user_content.reviews import Review, ReviewValue
from src.services.review import ReviewService
from tests.unit.src.core.config import settings


class TestReviewService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        client = AsyncIOMotorClient(settings.test_mongo_url)
        self.service = ReviewService(client.test_ugc)
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
