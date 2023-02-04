from datetime import datetime
from typing import Any, Optional, Protocol, runtime_checkable
from uuid import UUID

from pydantic import Field

from .base import ContentType, StrObjectId


@runtime_checkable
class UserContent(Protocol):
    """Интерфейс пользовательского контента.

    Описывает поля и методы общие для классов пользовательского
    контента: лайков, закладок, рейтингов, обзоров.
    """

    id: Optional[StrObjectId] = Field(alias='_id')
    created_at: Optional[datetime]
    user_id: UUID
    type: ContentType = ContentType
    target_id: StrObjectId
    target_type: ContentType = ContentType

    def __init__(self, **data: Any):
        """Создать объект с полями и значениями из data."""
        ...

    def dict(self) -> dict:
        """Вернуть поля класс их значения в виде dict."""
        ...
