from typing import Protocol
from uuid import UUID

from pydantic import BaseModel


class Event(Protocol):
    id: UUID
    event_type: str
    priority: str
    from_service: str
    details: BaseModel
