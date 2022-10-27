import uuid
from http import HTTPStatus

from core.db import db
from core.exceptions import BasicExceptionError
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from utils import messages as msg


class BaseModel(db.Model):
    """Модель, которая содержит некоторые общие базовые методы."""
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)

    @classmethod
    def save(cls):
        """Закоммитить сессию."""
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise BasicExceptionError(
                f"{cls.__name__} {msg.not_saved}: {e}",
                HTTPStatus.INTERNAL_SERVER_ERROR
            ) from e
