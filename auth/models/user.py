import uuid

from core.db import db
from flask_security import UserMixin
from models import AdvanceModel, Role, roles_users
from services.user import UserService, get_user_service
from sqlalchemy.dialects.postgresql import UUID


class User(AdvanceModel, UserMixin):
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

    @property
    def services(self):
        services: UserService = get_user_service(
            user=self, role_model=Role
        )
        return services

    def __repr__(self):
        return f'<User {self.login}>'

    def __str__(self):
        return self.login

    def get_security_payload(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
        }
