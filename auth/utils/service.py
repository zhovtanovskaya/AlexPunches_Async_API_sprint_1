from flask_sqlalchemy import Pagination
from pydantic import BaseModel
from routers.v1.schemes.paginate import PaginationResponse


def paginator_to_response(paginator: Pagination,
                          results: list[BaseModel],
                          ) -> PaginationResponse:
    return PaginationResponse(
        total=paginator.total,
        page=paginator.page,
        pages=paginator.pages,
        results=results,
    )
