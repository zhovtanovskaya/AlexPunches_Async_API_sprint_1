from fastapi import APIRouter, Depends, Request, Response, status

from src.api.v1.schemes.bookmark import (BookmarkCreateScheme,
                                         BookmarkResultsListScheme,
                                         BookmarkScheme)
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
    bookmark: BookmarkCreateScheme,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> BookmarkScheme:
    bookmark.user_id = request.state.user_id
    bookmark_model = transform_bookmark_scheme_to_model(bookmark)
    new_bookmark = await bookmark_service.create(obj=bookmark_model)
    return transform_bookmark_model_to_scheme(new_bookmark)


@router.get('', dependencies=[Depends(subscription_required)])
async def get_user_bookmark(
    request: Request,
    sort: str = '_id',
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> BookmarkResultsListScheme:
    bookmarks = bookmark_service.get_all(
        page_size=0,
        sort=sort,
        filters={'user_id': str(request.state.user_id)},
    )
    return BookmarkResultsListScheme(
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
