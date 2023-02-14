"""Сущности, общие для всех сервисов пользовательского контента."""

from typing import Any, AsyncIterable, Mapping

import pymongo
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import NonNegativeInt, PositiveInt

from src.services.ugc.models.protocols import UserContent


class ReactionService:
    """Сервис с общими операциями над пользовательским контентом."""

    user_content_type: UserContent

    def __init__(self, mongo: AsyncIOMotorDatabase):
        """Проинициализировать подключение к БД и коллекцию."""
        self.mongo = mongo
        self.collection = self.mongo.reactions

    async def get(self, id: ObjectId) -> UserContent | None:
        """Получить объект из базы данных.

        Поля _id и id будут содержать одинаковый
        ObjectId документа.
        """
        doc = await self.collection.find_one({'_id': ObjectId(id)})
        return self.to_obj(doc) if doc else None

    async def get_all(
        self,
        sort: str | None = None,
        filters: Mapping[str, Any] | None = None,
        page_number: PositiveInt = 1,
        page_size: NonNegativeInt = 50,
    ) -> AsyncIterable:
        """Получить список объектов на странице."""
        content_type_name = self.user_content_type.__fields__[
            'type'
        ].default
        find_filter = {'type': content_type_name}
        if filters is not None:
            find_filter.update(filters)
        result = self.collection.find(find_filter)

        if sort is not None:
            result = result.sort(sort, pymongo.DESCENDING)

        offset = page_size * (page_number - 1)
        async for doc in result.skip(offset).limit(page_size):
            yield self.to_obj(doc)

    async def create(self, obj: UserContent) -> UserContent | None:
        """Создать объект в базе данных.

        Поля obj.id не будет в документе БД.
        """
        obj_dict = obj.dict(exclude={'id': True}, exclude_none=True)
        result = await self.collection.insert_one(obj_dict)
        if result.acknowledged:
            return await self.get(result.inserted_id)
        return None

    async def delete(
              self,
              id: ObjectId,
              filters: Mapping[str, Any] | None = None,
    ) -> bool:
        """Удалить объект из базы данных.

        Returns:
            True -- если объект удален успешно.
        """
        delete_filter = {'_id': ObjectId(id)}
        if filters is not None:
            delete_filter.update(filters)
        result = await self.collection.delete_one(delete_filter)
        return result.deleted_count == 1

    def to_obj(self, doc: dict) -> UserContent:
        """Превратить в Python-объект документ MongoDB."""
        return self.user_content_type(**doc)
