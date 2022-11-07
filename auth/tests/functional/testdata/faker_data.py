"""Генератор фейковых данных."""
from functools import lru_cache

from faker import Faker
from functional.settings import test_settings
from functional.testdata.models import BaseDt, Role, RoleUser, User

fake = Faker()
Faker.seed(0)


class FakerData:
    """Фейковые данные для тестов.

    !Изменение COUNT_* констант может неожиданно повлиять на значения в данных.
    """

    COUNT_USERS = 100
    COUNT_ROLES = 10
    COUNT_ROLES_USERS = 250

    def __init__(self):
        """Создать фейковые данные для таблиц."""
        self.users = self.make_users()
        self.roles = self.make_roles()
        self.roles_users = self.make_roles_users(self.COUNT_ROLES_USERS)

    def get_data_by_table_name(self, table_name: str) -> list[BaseDt] | None:
        """Получить фейковые данные по названию таблицы."""
        if table_name == test_settings.users_tablename:
            return self.users
        if table_name == test_settings.roles_tablename:
            return self.roles
        if table_name == test_settings.roles_users_tablename:
            return self.roles_users
        return None

    def make_users(self) -> list[User]:
        """Создать тестовых данных для таблицы users."""
        return [User(
            id=fake.uuid4(),
            email=fake.email(),
            login=fake.user_name(),
            active=fake.pybool(),
            password=fake.password(length=10),
            fs_uniquifier=fake.pystr(),
        ) for _ in range(self.COUNT_USERS)]

    def make_roles(self) -> list[Role]:
        """Создать тестовых данных для таблицы roles."""
        return [Role(
            id=x + 1,
            name=fake.word(),
            description=fake.text(max_nb_chars=80),
        ) for x in range(self.COUNT_ROLES)]

    def make_roles_users(self, count) -> list[RoleUser]:
        """Создать тестовых данных для таблицы roles_users."""
        pass


@lru_cache()
def get_faker_data() -> FakerData:
    """Сделать синглтоном."""
    return FakerData()
