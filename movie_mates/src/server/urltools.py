__all__ = ['get_room_name']

def get_room_name(path: str):
    """Получить имя комнаты из пути URL `path`."""
    return path.strip().strip('/')