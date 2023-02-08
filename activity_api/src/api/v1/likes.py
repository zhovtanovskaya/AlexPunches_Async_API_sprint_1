from fastapi import APIRouter, Depends

from db.mongo import get_mongo_db
from services.like import get_like_service

router = APIRouter()


@router.delete('/{like_id}')
async def delete_like(
        like_id: str,
        db = Depends(get_mongo_db),
        service = Depends(get_like_service),
        ) -> None:
    async for doc in db.reactions.find({'type': 'like'}):
        print(doc)
    return None