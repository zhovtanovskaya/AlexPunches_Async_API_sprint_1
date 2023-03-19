from typing import Any, Mapping

from pydantic import BaseModel, Field

from core.config import EventTypes


class BaseMessage(BaseModel):
    event_type: EventTypes
    payload: BaseModel


class ChatMessagePayload(BaseModel):
    message: str = Field(..., max_length=300)


class ChatMessage(BaseMessage):
    event_type: EventTypes = EventTypes.chat_message
    payload: ChatMessagePayload
