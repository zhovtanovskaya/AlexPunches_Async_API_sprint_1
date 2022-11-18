import uuid
from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from core.db import db
from models import BaseModel


def create_partition(target, connection, **kw) -> None:
    """ creating partition by user_sign_in """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_smart" PARTITION OF "login_history" FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_mobile" PARTITION OF "login_history" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_web" PARTITION OF "login_history" FOR VALUES IN ('web')"""
    )


class LoginHistory(BaseModel):
    """Модель LoginHistory.
    """
    __tablename__ = 'login_history'
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create', create_partition)],
        }
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
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
