"""Трансофмации из схем в модели и наоборот."""
from .spawn_point import SpawnPointScheme
from models import SpawnPointModel


def transform_point_scheme_to_model(scheme: SpawnPointScheme,
                                    ) -> SpawnPointModel:
    """Трансформировать из схемы в модель."""
    return SpawnPointModel(
        film_id=scheme.film_id,
        time=scheme.time,
    )
