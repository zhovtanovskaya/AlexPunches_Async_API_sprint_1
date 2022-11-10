"""Дата-классы для данных для тестовой БД."""

from dataclasses import dataclass, fields
from datetime import datetime


@dataclass(slots=True)
class BaseDt:
    """Базовый класс с полезными общими методами."""

    @classmethod
    def get_fields(cls) -> list[str]:
        """Получить список полей дата-класса."""
        return [column.name for column in fields(cls)]

    @property
    def as_tuple(self) -> tuple[str, ...]:
        """Получить в виде tuple."""
        return tuple([self.__getattribute__(col) for col in self.get_fields()])


@dataclass(slots=True)
class User(BaseDt):
    """Дата-класс Пользователь."""

    id: str
    email: str
    login: str
    active: str
    password: str


@dataclass(slots=True)
class Role(BaseDt):
    """Дата-класс Роль."""

    id: str
    name: str
    description: str


@dataclass(slots=True)
class RoleUser(BaseDt):
    """Дата-класс сущности Юзер-роль. Связь M2M."""

    user_id: str
    role_id: str


@dataclass(slots=True)
class LoginHistory(BaseDt):
    """Дата-класс истории логинов."""

    id: str
    username: str
    email: str
    date_login: datetime
