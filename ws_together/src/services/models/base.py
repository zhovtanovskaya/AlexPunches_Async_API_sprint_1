from pydantic import BaseModel

from services.models.enums import EventTypes


class BaseMessage(BaseModel):
    event_type: EventTypes
    payload: BaseModel
