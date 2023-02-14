from functools import lru_cache
from typing import Type

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.mongo import get_mongo_db
from src.services.ugc.base import ReactionService
from src.services.ugc.models.bookmarks import Bookmark


class BookmarkService(ReactionService):

    user_content_type = Bookmark


@lru_cache()
def get_bookmark_service(
    mongo: AsyncIOMotorDatabase = Depends(get_mongo_db)
) -> BookmarkService:
    return BookmarkService(mongo)
