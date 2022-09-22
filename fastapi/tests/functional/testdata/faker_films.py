from faker import Faker

fake = Faker()
Faker.seed(0)


class FakerFilms:
    def __init__(self, genre_count: int, person_count: int, film_count: int):
        self.genres = self.make_genres(genre_count)
        self.persons = self.make_persons(person_count)
        self.films = self.make_films(film_count)

    @staticmethod
    def make_genres(genres_count: int) -> list:
        return [{
            "id": fake.uuid4(),
            "name": fake.words(nb=1, unique=True)[0],
            "description": fake.text(max_nb_chars=100),
        } for _ in range(genres_count)]

    @staticmethod
    def make_persons(presons_count: int) -> list:
        return [{
            "id": fake.uuid4(),
            "name": fake.name(),
        } for _ in range(presons_count)]

    def make_films(self, films_count: int) -> list:
        return [self._make_a_film() for _ in range(films_count)]

    def _make_a_film(self) -> dict[str, str | list]:
        film_genres = fake.random_elements(
            elements=self.genres, length=fake.random_int(min=1, max=5),
            unique=True)
        film_persons = fake.random_elements(
            elements=self.persons, length=fake.random_int(min=5, max=10),
            unique=True)
        film_directors = fake.random_elements(
            elements=film_persons, length=fake.random_int(min=1, max=5),
            unique=True)
        film_actors = fake.random_elements(
            elements=film_persons, length=fake.random_int(min=1, max=5),
            unique=True)
        film_writers = fake.random_elements(
            elements=film_persons, length=fake.random_int(min=1, max=5),
            unique=True)

        for genre in film_genres:
            genre.pop('description', None)

        return {
            'id': fake.uuid4(),
            'imdb_rating': fake.randomize_nb_elements(
                number=70, min=10, max=100,) / 10,
            'title': fake.sentence(nb_words=4)[:-1],
            'description': fake.text(max_nb_chars=150),
            'genre': [genre['name'] for genre in film_genres],
            'director':
                ' '.join([director['name'] for director in film_directors]),
            'actors_names':
                ' '.join([actor['name'] for actor in film_actors]),
            'writers_names':
                ' '.join([writer['name'] for writer in film_writers]),
            'directors': film_directors,
            'actors': film_actors,
            'writers': film_writers,
            'genres': film_genres,
        }
