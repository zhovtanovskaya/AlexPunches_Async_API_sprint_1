"""Партиции для таблицы login_history."""
from enum import Enum

from sqlalchemy import DDL, event

from models import BaseModel, LoginHistory, LoginHistoryMixin


class DeviceType(Enum):
    """Типы девайсов."""

    mobile = 'mobile'
    smart = 'smart'
    web = 'web'


def create_table_login_history_partition_ddl(
    table: str, device_type: DeviceType,
) -> None:
    """Функция, которая готовит DDL объекты по созданию секций.

    Для таблицы login_history по значению DeviceType.
    """
    return DDL(
        """
        CREATE TABLE IF NOT EXISTS %s
        PARTITION OF login_history FOR VALUES IN (\'%s\');
        """ % (table, device_type.value),
    ).execute_if(dialect='postgresql')


class LoginHistorySmartphone(LoginHistoryMixin, BaseModel):
    """User login history model for partition table for smartphone devices."""

    __tablename__ = 'login_history_smart'


class LoginHistoryWeb(LoginHistoryMixin, BaseModel):
    """User login history model for partition table for web devices."""

    __tablename__ = 'login_history_web'


class LoginHistoryMobile(LoginHistoryMixin, BaseModel):
    """User login history model for partition table for mobile devices."""

    __tablename__ = 'login_history_mobile'


PARTITION_TABLES_REGISTRY = (
    (LoginHistorySmartphone, DeviceType.smart),
    (LoginHistoryWeb, DeviceType.web),
    (LoginHistoryMobile, DeviceType.mobile),
)


def attach_event_listeners() -> None:
    """Функция, которая автоматически заполняет партиционные таблице.

    По каждой модели от корневой loginhistory.
    """
    for class_, device_type in PARTITION_TABLES_REGISTRY:
        class_.__table__.add_is_dependent_on(LoginHistory.__table__)
        event.listen(
            class_.__table__,
            'after_create',
            create_table_login_history_partition_ddl(
                class_.__table__, device_type,
            ),
        )


attach_event_listeners()
