from pydantic import BaseModel

from services.models.base import BaseMessage
from services.models.enums import EventTypes, PlayerStatuses, PlayerType


class PlayerStatePayload(BaseModel):
    player_type: PlayerType | None = None
    timecode: float | None = None
    player_status: PlayerStatuses | None = None
    speed: float = 1.0


class PlayerStateScheme(BaseMessage):
    event_type: EventTypes = EventTypes.player_state
    payload: PlayerStatePayload = PlayerStatePayload()
