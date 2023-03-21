from pydantic import BaseModel, Field

from services.models.base import BaseMessage
from services.models.enums import EventTypes


class ChatMessagePayload(BaseModel):
    message: str = Field(..., max_length=300)
    from_user: str | None = None


class ChatMessageScheme(BaseMessage):
    event_type: EventTypes = EventTypes.broadcast_message
    payload: ChatMessagePayload
