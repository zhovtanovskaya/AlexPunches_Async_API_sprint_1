from core.db import db
from sqlalchemy.dialects.postgresql import UUID

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
)
