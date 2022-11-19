import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DDL, UniqueConstraint, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from core.db import db
from models import BaseModel


class DeviceType(Enum):
    mobile = "mobile"
    smart = "smart"
    web = "web"


def create_table_login_history_partition_ddl(
    table: str, device_type: DeviceType
) -> None:
    return DDL(
        """
        ALTER TABLE login_history ATTACH PARTITION %s FOR VALUES IN ('%s');"""
        % (table, device_type)
    ).execute_if(dialect="postgresql")


class LoginHistoryMixin:
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)

    @declared_attr
    def user_id(self):
        return db.Column(
            UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE")
        )

    email = db.Column(db.String, nullable=False)
    date_login = db.Column(db.DateTime(), default=datetime.utcnow)
    user_agent = db.Column(db.Text)
    user_device_type = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        """Вернуть repr()."""
        return (
            f'Login history (id={self.id!r}, '
            f'mail={self.email!r})'
        )

    def as_value(self) -> str:
        return self.event_type.value


class LoginHistory(LoginHistoryMixin, BaseModel):
    """Модель LoginHistory.
    """
    __tablename__ = 'login_history'
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
        }
    )


class LoginHistorySmartphone(LoginHistoryMixin, BaseModel):
    """User login history model for partition table for smartphone devices."""

    __tablename__ = "login_history_smart"


class LoginHistoryWeb(LoginHistoryMixin, BaseModel):
    """User login history model for partition table for web devices."""

    __tablename__ = "login_history_web"


class LoginHistoryMobile(LoginHistoryMixin, BaseModel):
    """User login history model for partition table for mobile devices."""

    __tablename__ = "login_history_mobile"


PARTITION_TABLES_REGISTRY = (
    (LoginHistorySmartphone, 'smart'),
)


def attach_event_listeners() -> None:
    for class_, device_type in PARTITION_TABLES_REGISTRY:
        class_.__table__.add_is_dependent_on(LoginHistory.__table__)
        event.listen(
            class_.__table__,
            "after_create",
            create_table_login_history_partition_ddl(
                class_.__table__, device_type
            ),
        )


attach_event_listeners()
