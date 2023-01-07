"""Модели активностей."""

from uuid import UUID

from pydantic import BaseModel


class SpawnPointModel(BaseModel):
    """Модель момента фильма, во время просмотра пользователем."""

    user_id: UUID | None = None
    film_id: str
    time: int
