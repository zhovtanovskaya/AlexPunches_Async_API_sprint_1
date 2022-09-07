from api.v1.shemes.film import Film as FilmScheme
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


def es_genre_to_genre_scheme(es_genre: GenreModel) -> GenreScheme:
    return GenreScheme(
        uuid=es_genre.id,
        name=es_genre.name,
        description=es_genre.description
    )


def es_person_to_person_scheme(es_person: PersonModel) -> PersonScheme:
    return GenreScheme(
        id=es_person.id,
        name=es_person.name,
        role=es_person.role,
        film_ids=es_person.film_ids
    )
