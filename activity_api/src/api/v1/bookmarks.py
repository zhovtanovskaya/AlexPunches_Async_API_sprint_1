from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from pymongo.errors import DuplicateKeyError

import src.api.v1.schemes.bookmark as schemes
from src.api.v1.schemes.transform_schemes import (
    transform_bookmark_model_to_scheme, transform_bookmark_scheme_to_model)
from src.auth.request import subscription_required
from src.services.ugc.bookmark import BookmarkService, get_bookmark_service
from src.services.ugc.models.custom_types import StrObjectId

router = APIRouter()


@router.post(
    '',
    dependencies=[Depends(subscription_required)],
    status_code=status.HTTP_201_CREATED,
)
async def create_bookmark(
    request: Request,
    bookmark: schemes.BookmarkCreateScheme,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> schemes.BookmarkScheme:
    bookmark.user_id = request.state.user_id
    bookmark_model = transform_bookmark_scheme_to_model(bookmark)
    try:
        new_bookmark = await bookmark_service.create(obj=bookmark_model)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='DuplicateKeyError',
        )
    return transform_bookmark_model_to_scheme(new_bookmark)


@router.get('', dependencies=[Depends(subscription_required)])
async def get_user_bookmarks(
    request: Request,
    sort: str = '_id',
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> schemes.BookmarkResultsListScheme:
    bookmarks = bookmark_service.get_all(
        page_size=0,
        sort=sort,
        filters={'user_id': str(request.state.user_id)},
    )
    return schemes.BookmarkResultsListScheme(
        results=[
            transform_bookmark_model_to_scheme(bookmark)
            async for bookmark in bookmarks
        ],
    )


@router.delete('/{bookmark_id}', dependencies=[Depends(subscription_required)])
async def delete_bookmark(
    bookmark_id: StrObjectId,
    request: Request,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> Response:
    await bookmark_service.delete(
        id=bookmark_id,
        filters={'user_id': str(request.state.user_id)},
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
