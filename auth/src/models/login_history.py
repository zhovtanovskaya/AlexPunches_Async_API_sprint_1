"""Модель истории логинов для БД."""
import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from core.db import db
from models import BaseModel


class LoginHistory(BaseModel):
    """Модель LoginHistory."""

    __tablename__ = 'login_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    date_login = db.Column(db.DateTime(), default=datetime.utcnow)
    # не решил нужна ли перекрестая ссылка на пользователя
    # user = db.relationship(
    #   'User', secondary=users_login_histories, lazy="subquery",
    #   backref=db.backref('login_histories', lazy='subquery'))

    def __repr__(self):
        """Вернуть repr()."""
        return (
            f'Login history (id={self.id!r}, '
            f'mail={self.email!r})'
        )
