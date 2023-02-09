from src.services.ugc.like import LikeService
from src.services.ugc.models.user_content.likes import Like, LikeValue
from tests.unit.src.base import ReactionTestCase


class TestLikeService(ReactionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.service = LikeService(self.db)
        self.like = Like(
            user_id='af18023d-9c76-11ed-9485-7831c1bc31e4',
            target_id='63d0c92bf5eb85d9a10bd8ac',
            value=LikeValue.LIKE,
        )

    async def test_create(self):
        new_like = await self.service.create(self.like)
        self.assertIsNotNone(await self.service.get(new_like.id))

    async def test_delete(self):
        new_like = await self.service.create(self.like)
        await self.service.delete(new_like.id)
        self.assertIsNone(await self.service.get(new_like.id))
