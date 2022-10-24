from core.db import db
from flask_security import RoleMixin
from models import AdvanceModel


class Role(AdvanceModel, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
