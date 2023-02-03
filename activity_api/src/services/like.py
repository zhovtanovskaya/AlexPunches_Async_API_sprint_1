from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .models.user_content import Like


class LikeService:

    def __init__(self, mongo: AsyncIOMotorDatabase):
        self.mongo = mongo
        self.collection = self.mongo['reactions']

    def create(self, obj: Like) -> Like:
        return Like()

    async def delete(self, id: str):
        result = await self.mongo['reactions'].delete_one({'_id': ObjectId(id)})
        assert result.deleted_count == 1, result.deleted_count
