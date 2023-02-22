from datetime import datetime

from core.config import config


def is_night(time: datetime) -> bool:
    """Получить True, если время ночное."""
    return (
        config.night_stop_hour > time.hour
        or time.hour > config.night_start_hour
    )
