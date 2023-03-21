from services.models.enums import EventTypes
from services.models.player_state import PlayerStatePayload, PlayerStateScheme
from services.ws_data import RoomState


def room_state_to_player_state_scheme(
          room_state: RoomState,
) -> PlayerStateScheme:
    payload = PlayerStatePayload(
        speed=room_state.speed,
        timecode=room_state.timecode,
        player_status=room_state.player_status,
    )
    return PlayerStateScheme(
        event_type=EventTypes.player_state,
        payload=payload,
    )


def player_state_scheme_to_room_state(scheme: PlayerStateScheme) -> RoomState:
    return RoomState(
        speed=scheme.payload.speed,
        timecode=scheme.payload.timecode,
        player_status=scheme.payload.player_status,
    )
