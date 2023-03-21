from enum import Enum


class EventTypes(str, Enum):
    # Сообщения в чат
    broadcast_message = 'broadcast_message'
    # Команды на все плееры в руме (pause, play, ...)
    broadcast_command = 'broadcast_command'
    # Запросы WS-серверу (get_room_state, get_player_state, ...)
    room_request = 'room_request'
    # история всех сообщений чата для комнаты
    chat_state = 'chat_state'
    # состояние плеера (timestamp, и статус "ведущий")
    player_state = 'player_state'
    # Сообщение об ошибке (для клиента)
    error = 'error'


class PlayerStatuses(str, Enum):
    pause = 'pause'
    play = 'play'
    stop = 'stop'


class RoomRequests(str, Enum):
    get_chat_state = 'get_chat_state'
    get_player_state = 'get_player_state'
    set_state = 'set_state'


class PlayerType(str, Enum):
    lead = 'lead'
    watcher = 'watcher'
