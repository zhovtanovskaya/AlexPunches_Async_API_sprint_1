"""Трансофмации из схем в модели и наоборот."""
from src.api.v1.schemes.spawn_point import SpawnPointScheme
from src.services.activity.models.spawn_point import SpawnPointModel


def transform_point_scheme_to_model(scheme: SpawnPointScheme,
                                    ) -> SpawnPointModel:
    """Трансформировать из схемы в модель."""
    return SpawnPointModel(
        film_id=scheme.film_id,
        time=scheme.time,
    )
