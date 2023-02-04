"""Генератор фейковых данных.

При seed(0), юзеров 1К, фильмов 1К
получаем 111_168_000 штук.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, List

from bson.objectid import ObjectId
from config import logger
from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()
Faker.seed(0)


@dataclass
class User:
    """Дата-класс Пользователь."""

    id: str


@dataclass
class Film:
    """Дата-класс Фильм."""

    id: str


class Reaction(BaseModel):
    """Пидантик-класс Реакции (оценка, рецензия, лайк) на что-либо.

    Пидантик потому что удобно исключить неустановленные свойства
    reaction.dict(exclude_none=True).
    """

    id: str = Field(alias="_id")
    created_at: datetime
    user_id: str
    target_id: str
    target_type: str
    type: str
    value: int
    title: str | None = None
    text: str | None = None


def create_users(count: int) -> List[User]:
    """Создать список юзеров."""
    return [User(id=str(fake.uuid4())) for _ in range(count)]


def create_films(count: int) -> List[Film]:
    """Создать список фильмов."""
    return [Film(id=str(fake.uuid4())) for _ in range(count)]


def generate_user_content(users_count: int, films_count: int) -> Generator:
    """Сгенерировать реакцию.

    Получается, что каждый юзер поставит оценку каждому фильму,
    каждый юзер напишет рецензию каждому фильму,
    каждый юзер поставит лайк/дизлайк каждой рецензии.
    """
    users = create_users(users_count)
    films = create_films(films_count)

    guc_count = 0
    # будем копить все ревью (только свойства: id и created_at).
    # Всего users_count * films_count штук. !Угроза для памяти.
    light_reviews_list = []

    for user in users:
        guc_at_time = datetime(2022, 1, 1, 0, 0, 1) + timedelta(minutes=30)
        for film in films:
            guc_at_time += timedelta(minutes=7)
            # сделать реакцию
            yield Reaction(
                _id=str(ObjectId()),
                created_at=guc_at_time,
                user_id=user.id,
                target_id=film.id,
                target_type='movie',
                type='rating',
                value=fake.random_int(min=0, max=10),
            )
            guc_count += 1
            guc_at_time += timedelta(minutes=41)
            # сделать рецензию
            review_obj = Reaction(
                _id=str(ObjectId()),
                created_at=guc_at_time,
                user_id=user.id,
                target_id=film.id,
                target_type='movie',
                type='review',
                value=fake.random_element(elements=(0, 5, 10)),
                title=fake.sentence(nb_words=7),
                text=fake.text(max_nb_chars=1000),
            )
            light_reviews_list.append({
                'id': review_obj.id,
                'created_at': review_obj.created_at,
                'user_id': review_obj.user_id,
            })
            yield review_obj
            guc_count += 1

    for user in users:
        for review in light_reviews_list:
            if review['user_id'] != user.id:
                minutes = fake.random_int(min=10, max=120, step=8)
                guc_at_time = review['created_at'] + timedelta(minutes=minutes)
                # поставить лайк/дизлайк на рецензию
                yield Reaction(
                    _id=str(ObjectId()),
                    created_at=guc_at_time,
                    user_id=user.id,
                    target_id=review['id'],
                    target_type='review',
                    type='like',
                    value=fake.random_element(elements=(0, 10)),
                )
                guc_count += 1

    logger.info(f'готово guc: {guc_count} штук')
