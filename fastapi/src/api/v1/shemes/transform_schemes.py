from typing import Type

from pydantic import BaseModel

from api.v1.shemes.film import Film as FilmScheme
from api.v1.shemes.film import FilmShort
from api.v1.shemes.genre import Genre as GenreScheme
from api.v1.shemes.genre import GenreShort
from api.v1.shemes.person import Person as PersonScheme
from api.v1.shemes.person import PersonShort
from models.film import Film as FilmModel
from models.genre import Genre as GenreModel
from models.person import Person as PersonModel


def es_film_to_film_scheme(es_film: FilmModel) -> FilmScheme:
    return FilmScheme(
        uuid=es_film.id,
        title=es_film.title,
        imdb_rating=es_film.imdb_rating,
        description=es_film.description,
        genre=[GenreShort(**genre.dict()) for genre in es_film.genres],
        actors=[PersonShort(**actor.dict()) for actor in es_film.actors],
        writers=[PersonShort(**writer.dict()) for writer in es_film.writers],
        directors=[
            PersonShort(**director.dict()) for director in es_film.directors],
    )


def es_film_to_film_short_scheme(es_film: FilmModel) -> FilmShort:
    return FilmShort(
        uuid=es_film.id,
        title=es_film.title,
        imdb_rating=es_film.imdb_rating,
    )


def es_genre_to_genre_scheme(es_genre: GenreModel) -> GenreScheme:
    return GenreScheme(
        uuid=es_genre.id,
        name=es_genre.name,
        description=es_genre.description
    )


def es_person_to_person_scheme(es_person: PersonModel) -> PersonScheme:
    return PersonScheme(
        id=es_person.id,
        name=es_person.name,
        role=es_person.role,
        film_ids=es_person.film_ids
    )


def api_field_name_to_es_field_name(
          api_field_name: str,
          api_scheme: Type[BaseModel],
) -> str:
    """Перевести имя поля из АПИ-схемы в соответствующе имя Эластик-схемы.

    Нужно, например, для того, чтобы возможно было
        сортировать по названиям полей из АПИ схемы, а не из Эластика.

    Если есть поле с алиасом <field>, то вернем название этого поля.
    Не теряем
        - признак сортировки в начале строки. "-" или "" (минус или пусто)
        - название вложенного поля. После "." (точки) в имени.
            чтобы использовать типичные подполя, например, .raw,
            не заглядывая в схему Эластика.
    """
    prefix = ''
    if api_field_name[0] == '-':
        api_field_name = api_field_name[1:]
        prefix = '-'

    name_splited = api_field_name.split('.', 1)
    for k, v in api_scheme.__fields__.items():
        if v.alias == name_splited[0]:
            name_splited[0] = k
    es_field_name = '.'.join(name_splited)
    return f'{prefix}{es_field_name}'
