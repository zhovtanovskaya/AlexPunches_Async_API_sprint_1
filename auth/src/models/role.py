from flask_security import RoleMixin

from core.db import db
from models import BaseModel


class Role(BaseModel, RoleMixin):
    """Роли пользователей.

    В проекте используем библиотеку flask-security-too
    базовый набор полей Ролей зависит от нее
    https://flask-security-too.readthedocs.io/en/stable/models.html
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
