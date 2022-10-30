import uuid

from core.db import db
from flask_security import UserMixin
from models import BaseModel, roles_users
from sqlalchemy.dialects.postgresql import UUID


class User(BaseModel, UserMixin):
    """Модель пользователя.
    В проекте используем библиотеку flask-security-too
    базовый набор полей Пользователя зависит от нее
    https://flask-security-too.readthedocs.io/en/stable/models.html
    """
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, lazy="subquery",
                            backref=db.backref('users', lazy='subquery'))

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    def get_security_payload(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
        }
