from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .models.user_content import Like


class LikeService:

    def __init__(self, mongo: AsyncIOMotorDatabase):
        self.mongo = mongo
        self.collection = self.mongo.reactions

    async def get(self, id: str):
        doc = await self.collection.find_one({'_id': ObjectId(id)})
        return Like(**doc) if doc else None

    async def create(self, obj: Like) -> Like:
        obj_dict = obj.dict()
        del obj_dict['id']
        result = await self.collection.insert_one(obj_dict)
        if result.acknowledged:
            return await self.get(result.inserted_id)

    async def delete(self, id: str):
        result = await self.collection.delete_one({'_id': ObjectId(id)})
        assert result.deleted_count == 1, result.deleted_count
