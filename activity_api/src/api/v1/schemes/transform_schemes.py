"""Трансофмации из схем в модели и наоборот."""
from api.v1.schemes.spawn_point import SpawnPointScheme
from models import SpawnPointModel


def transform_point_scheme_to_model(scheme: SpawnPointScheme,
                                    ) -> SpawnPointModel:
    """Трансформировать из схемы в модель."""
    return SpawnPointModel(
        user_id=scheme.user_id,
        film_id=scheme.film_id,
        time=scheme.time,
    )
