from typing import AsyncIterable

from .base import ReactionService
from .models.user_content.reviews import Review


class ReviewService(ReactionService):

    user_content_type = Review

    async def get_all(self) -> AsyncIterable:
        result = self.collection.find({'type':  'review'})
        async for doc in result:
            yield self.to_obj(doc)
