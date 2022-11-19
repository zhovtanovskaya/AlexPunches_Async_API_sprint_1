import pytest

from functional.testdata import determination_data, faker_films


@pytest.fixture
def es_determination_data() -> dict:
    """Подготовить заранее определенные конкретные данные.
    :return: dict(
                 films: list,     # 10 штук
                 genres: list,    # 10 штук
                 persons: list,   # 10 штук
                )
    """
    return {
        'genres': determination_data.genres,
        'persons': determination_data.persons,
        'films': determination_data.films,
    }


@pytest.fixture
def es_fake_data_fix_count(faker) -> dict:
    """Подготовить фейковые данные в определенном количестве.
    :return: dict(
                 genres: list,    # 100 штук
                 persons: list,   # 100 штук
                 films: list,     # 1000 штук
                )
    """
    fake_films = faker_films.FakerFilms(
        genre_count=10 ** 2,
        person_count=10 ** 2,
        film_count=10 ** 3,
    )
    return {
        'genres': fake_films.genres,
        'persons': fake_films.persons,
        'films': fake_films.films,
    }
