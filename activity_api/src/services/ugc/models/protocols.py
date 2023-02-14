from datetime import datetime
from typing import Any, Optional, Protocol, runtime_checkable
from uuid import UUID

from pydantic import Field

from src.services.ugc.models.base import ContentType, StrObjectId


@runtime_checkable
class UserContent(Protocol):
    """Интерфейс пользовательского контента.

    Описывает поля и методы общие для классов пользовательского
    контента: лайков, закладок, рейтингов, обзоров.
    """

    # Ожидается имя типа пользовательского
    # контента в .__fields__['type'].  Например,
    # "review", "like".
    __fields__: dict

    id: Optional[StrObjectId] = Field(alias='_id')
    created_at: Optional[datetime]
    user_id: UUID
    type: ContentType
    target_id: StrObjectId | UUID
    target_type: ContentType

    def __init__(self, **data: Any):
        """Создать объект с полями и значениями из data."""
        ...

    def dict(self, *args, **kwargs) -> dict:
        """Вернуть поля класс их значения в виде dict."""
        ...
