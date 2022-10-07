from auth_models import AdvanceModel
from core.db import db
from flask_security import RoleMixin


class Role(AdvanceModel, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self,
                 name: str | None = None,
                 description: str | None = None
                 ):
        self.description = description
        self.name = name
