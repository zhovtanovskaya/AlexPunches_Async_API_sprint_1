from app import config
from pydantic import BaseModel, conint


class PaginationQuery(BaseModel):
    page: conint(ge=1) | None = config.paginator_start_page
    per_page: conint(ge=1, le=100) | None = config.paginator_per_page


class PaginationResponse(BaseModel):
    total: int
    page: conint(ge=1)
    pages: conint(ge=0)
    results: list[BaseModel]
