"""Трансофмации из схем в модели и наоборот."""
from models import SpawnPointModel

from .spawn_point import SpawnPointScheme


def transform_point_scheme_to_model(scheme: SpawnPointScheme,
                                    ) -> SpawnPointModel:
    """Трансформировать из схемы в модель."""
    return SpawnPointModel(
        film_id=scheme.film_id,
        time=scheme.time,
    )
