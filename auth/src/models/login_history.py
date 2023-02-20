"""Модели истории входов на сервис."""

import uuid
from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from db.db import db
from models import BaseModel


class LoginHistoryMixin:
    """Микшин чтобы в партициях использовать."""

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
        nullable=False)

    @declared_attr
    def user_id(self):
        """ИД юзера."""
        return db.Column(
            UUID(as_uuid=True), db.ForeignKey('users.id'),
        )

    email = db.Column(db.String, nullable=False)
    date_login = db.Column(db.DateTime(), default=datetime.utcnow)
    user_agent = db.Column(db.Text)
    user_device_type = db.Column(db.Text, nullable=False, primary_key=True)

    def __repr__(self):
        """Вернуть repr()."""
        return (
            f'Login history (id={self.id!r}, '
            f'mail={self.email!r})'
        )


class LoginHistory(LoginHistoryMixin, BaseModel):
    """История входов на сервис."""

    __tablename__ = 'login_history'
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
        },
    )
