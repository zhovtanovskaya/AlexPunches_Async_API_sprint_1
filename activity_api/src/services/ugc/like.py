from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.mongo import get_mongo_db
from src.services.ugc.base import ReactionService
from src.services.ugc.models.likes import Like


class LikeService(ReactionService):

    user_content_type = Like


@lru_cache()
def get_like_service(
    mongo: AsyncIOMotorDatabase = Depends(get_mongo_db)
) -> LikeService:
    return LikeService(mongo)
