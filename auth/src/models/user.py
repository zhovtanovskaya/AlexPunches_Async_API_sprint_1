"""SQLAlchemy-модель Пользователя для БД."""

import uuid

from sqlalchemy.dialects.postgresql import UUID

from core.db import db
from models import BaseModel, roles_users


class User(BaseModel):
    """Модель пользователя.

    В проекте используем библиотеку flask-security-too
    базовый набор полей Пользователя зависит от нее
    https://flask-security-too.readthedocs.io/en/stable/models.html
    """

    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    email_confirmation = db.Column(db.Boolean, default=False, nullable=True)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, lazy='subquery',
                            backref=db.backref('users', lazy='subquery'))
    confirmation_code = db.Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=True,
    )

    def __str__(self):
        """Вернуть в виде строки."""
        return self.email

    def __repr__(self):
        """Вернуть в виде строки."""
        return f'<User {self.email}>'
