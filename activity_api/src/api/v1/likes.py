from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.mongo import get_mongo_db

router = APIRouter()


@router.delete('/{like_id}')
async def delete_like(
        like_id: str,
        db: AsyncIOMotorDatabase = Depends(get_mongo_db),
        ) -> None:
    async for doc in db.reactions.find({'type': 'like'}):
        print(doc)
    return None
