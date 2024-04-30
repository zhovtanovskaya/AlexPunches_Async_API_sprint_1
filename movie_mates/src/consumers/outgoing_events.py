"""Исходящие события от сервера клиенту через вебсокет."""

from pydantic import BaseModel

__all__ = ['IncomingTextEvent', 'ErrorEvent', 'ListUserNamesEvent']


class IncomingTextEvent(BaseModel):
    """Событие о новом сообщении в чате."""

    type: str = 'incoming_text'
    author: str
    text: str


class ErrorEvent(BaseModel):
    """Ответ об ошибке при обработке входящего события."""

    type: str = 'error'
    text: str
    on_event: str | dict


class ListUserNamesEvent(BaseModel):
    """Список имен пользователей в комнате."""

    type: str = 'list_user_names'
    user_names: list[str]
