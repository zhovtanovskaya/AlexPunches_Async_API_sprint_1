from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.mongo import get_mongo_db

from .base import ReactionService
from .models.user_content.likes import Like


class LikeService(ReactionService):

    user_content_type = Like


@lru_cache()
async def get_like_service(
        mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
        ) -> LikeService:
    return LikeService(mongo_db)
