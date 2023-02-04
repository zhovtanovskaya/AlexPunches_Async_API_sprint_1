from typing import Type

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .models.user_content.likes import Like
from .models.user_content.protocols import UserContent


class ReactionService:
    """Сервис с общими операциями над пользовательским контентом."""

    user_content_type: Type[UserContent]

    def __init__(self, mongo: AsyncIOMotorDatabase):
        """Проинициализировать подключение к БД и коллекцию."""
        self.mongo = mongo
        self.collection = self.mongo.reactions

    async def get(self, id: ObjectId) -> UserContent:
        """Получить документ из базы данных.

        Поля _id и id будут содержать одинаковый
        ObjectId документа.
        """
        doc = await self.collection.find_one({'_id': ObjectId(id)})
        return self.to_obj(doc) if doc else None

    async def create(self, obj: UserContent) -> UserContent:
        """Создать объект в базе данных.

        Поля obj.id не будет в документе БД.
        """
        obj_dict = obj.dict()
        del obj_dict['id']
        result = await self.collection.insert_one(obj_dict)
        if result.acknowledged:
            return await self.get(result.inserted_id)

    async def delete(self, id: ObjectId) -> bool:
        """Удалить объект из базы данных.

        Returns:
            True -- если объект удален успешно.
        """
        result = await self.collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count == 1

    def to_obj(self, doc: dict) -> UserContent:
        """Превратить в Python-объект документ MongoDB."""
        return self.user_content_type(**doc)


class LikeService(ReactionService):

    user_content_type = Like
