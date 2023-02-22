"""Генератор фейковых данных."""
from enum import Enum
from functools import lru_cache

from faker import Faker

from functional.settings import test_settings
from functional.testdata.models import (BaseDt, LoginHistory, Role, RoleUser,
                                        User)

fake = Faker()
Faker.seed(0)


class DeviceType(Enum):
    """Типы девайсов."""

    mobile = 'mobile'
    smart = 'smart'
    web = 'web'


class FakerData:
    """Класс Фейкомёт.

    Фейковые данные для тестов.
    !Изменение COUNT_* констант может неожиданно повлиять на значения в данных.
    Несмотря на то, что все данные детерменированы, все равно будем стараться
    избегать хардкода в тестах.

    Для Юзра[0](
    id='e3e70682-c209-4cac-a29f-6fbed82c07cd',
    email='gwilliams@example.com',
    login='thull',
    active=True,
    password='_9*lzGeq^*',
    )
    - создадим ровно 10 записей в истории логинов,
    - добавим ровно все 10 ролей
    """

    COUNT_USERS = 100
    COUNT_ROLES = 10
    COUNT_ROLES_USERS = 250
    COUNT_LOGIN_HISTORIES = 100

    def __init__(self):
        """Создать фейковые данные для таблиц."""
        self.users = self.make_users()
        self.roles = self.make_roles()
        self.roles_users = self.make_roles_users(self.COUNT_ROLES_USERS)
        self.login_histories = self.make_histories()

    def get_data_by_table_name(self, table_name: str) -> list[BaseDt] | None:
        """Получить фейковые данные по названию таблицы."""
        if table_name == test_settings.users_tablename:
            return self.users
        if table_name == test_settings.roles_tablename:
            return self.roles
        if table_name == test_settings.roles_users_tablename:
            return self.roles_users
        if table_name == test_settings.login_histories_tablename:
            return self.login_histories
        return None

    def make_users(self) -> list[User]:
        """Создать тестовых данных для таблицы users."""
        return [User(
            id=fake.uuid4(),
            email=fake.email(),
            active=fake.pybool(),
            is_email_confirmed=fake.pybool(),
            password=fake.password(length=10),
            confirmation_code=fake.uuid4(),
        ) for _ in range(self.COUNT_USERS)]

    def make_roles(self) -> list[Role]:
        """Создать тестовых данных для таблицы roles."""
        return [Role(
            id=x + 1,
            name=fake.word(),
            description=fake.text(max_nb_chars=80),
        ) for x in range(self.COUNT_ROLES)]

    def make_roles_users(self, count) -> list[RoleUser]:
        """Создать тестовых данных для таблицы roles_users.

        В которых у Юзера[0] будут все Роли. Всего COUNT_ROLES (10) штук.
        """
        pass

    def make_histories(self) -> list[LoginHistory]:
        """Создать тестовых данных для таблицы login_histories.

        В которой у Юзера[0] будет 10 записей в LoginHistory.
        """
        list_ints = []
        for _ in range(self.COUNT_LOGIN_HISTORIES):
            list_ints.append(fake.random_int(min=1, max=self.COUNT_USERS - 1))
        list_ints.extend([0] * 10)

        return [LoginHistory(
            id=fake.uuid4(),
            email=self.users[x].email,
            date_login=fake.date_time(),
            user_id=self.users[x].id,
            user_agent=fake.user_agent(),
            user_device_type=fake.random_element(elements=('smart', 'mobile', 'web')),  # noqa
        ) for x in list_ints]


@lru_cache()
def get_faker_data() -> FakerData:
    """Сделать синглтоном."""
    return FakerData()
