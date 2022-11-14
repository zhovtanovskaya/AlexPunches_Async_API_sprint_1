"""Схемы для постраничной разбивки."""

from pydantic import BaseModel, PositiveInt

from core.config import config


class Page(BaseModel):
    """Схема для валидации параметров, описывающих страницу в HTTP-запросе."""

    page_number: PositiveInt = config.paginator_start_page
    per_page: PositiveInt = config.paginator_per_page
