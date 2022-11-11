"""Дата-классы для данных для тестовой БД."""

from dataclasses import dataclass, fields


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

    def __post_init__(self):
        """Установить хэш пароля по умолчанию всем тестовым пользователям."""
        # Хэш пароля вычислен так:
        # werkzeug.security.generate_password_hash('password', method='sha256')
        self.password = (
            'sha256$'
            '5Q531DSL7FIi8aVB$'
            'eb5264e16a2bff7676f841877113f9f8f3c37c6694e6f731817a26d126f7e6ef'
        )


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
