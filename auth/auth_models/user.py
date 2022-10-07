import uuid
from http import HTTPStatus

from auth_models import AdvanceModel, roles_users
from core.db import db
from core.exceptions import BasicExceptionError
from flask_security import UserMixin
from flask_security.registerable import register_user
from routers.v1.schemes.users import UserCreate
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
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.login}>'

    @staticmethod
    def create_user(scheme: UserCreate):
        try:
            user = register_user(**scheme.dict())
        except Exception as e:
            db.session.rollback()
            raise BasicExceptionError(
                f"Error: {e}", HTTPStatus.BAD_REQUEST) from e
        else:
            user.save()
        return user

    def get_security_payload(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
        }
