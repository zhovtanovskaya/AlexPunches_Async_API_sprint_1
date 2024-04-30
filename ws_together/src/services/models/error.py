from pydantic import BaseModel

from services.models.base import BaseMessage
from services.models.enums import EventTypes


class ErrorPayload(BaseModel):
    message: str


class ErrorScheme(BaseMessage):
    event_type: EventTypes = EventTypes.error
    payload: ErrorPayload
