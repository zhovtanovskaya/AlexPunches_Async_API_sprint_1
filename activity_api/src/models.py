"""Модели активностей."""

from uuid import UUID

from pydantic import BaseModel


class ActivityModel(BaseModel):
    """Модель момента фильма, во время просмотра пользователем.

    Каждую минуту клиен отправляет данные, на каком моменте в данный момент
    находится просмотр фильма.
    Если пользователь аутентифицирован, то передается и юзер-ид.
    """

    user_id: UUID | None = None
    film_id: str
    time: int
