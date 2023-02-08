from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

mongo_db: Optional[AsyncIOMotorDatabase] = None


async def get_mongo_db() -> AsyncIOMotorDatabase:
    return mongo_db
