"""Дата-классы для данных для тестовой БД."""

from dataclasses import dataclass, fields
from datetime import datetime
from typing import Sequence

from werkzeug.security import generate_password_hash


@dataclass(slots=True)
class BaseDt:
    """Базовый класс с полезными общими методами."""

    @classmethod
    def get_fields(cls) -> list[str]:
        """Получить список полей дата-класса."""
        return [column.name for column in fields(cls) if column.type != Sequence]  # noqa

    @property
    def as_tuple(self) -> tuple[str, ...]:
        """Получить в виде tuple."""
        list_values = []
        for col in self.get_fields():
            value = self.__getattribute__(col)
            # хешировать пароль
            if col == 'password':
                value = generate_password_hash(password=value, method='sha256')
            list_values.append(value)
        return tuple(list_values)


@dataclass(slots=True)
class User(BaseDt):
    """Дата-класс Пользователь."""

    id: str
    email: str
    active: str
    email_confirmation: str
    confirmation_code: str
    password: str


@dataclass(slots=True)
class Role(BaseDt):
    """Дата-класс Роль."""

    name: str
    description: str
    id: Sequence


@dataclass(slots=True)
class RoleUser(BaseDt):
    """Дата-класс сущности Юзер-роль. Связь M2M."""

    user_id: str
    role_id: str


@dataclass(slots=True)
class LoginHistory(BaseDt):
    """Дата-класс истории логинов."""

    id: str
    email: str
    date_login: datetime
    user_id: str
    user_agent: str
    user_device_type: str
