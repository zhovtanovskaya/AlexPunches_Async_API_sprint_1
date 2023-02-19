from datetime import datetime

from core.config import config


def is_it_hight(time: datetime) -> bool:
    xz = (config.night_stop_hour > time.hour or time.hour > config.night_start_hour)
    return xz

