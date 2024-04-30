"""Исходящие события от сервера клиенту через вебсокет."""

from pydantic import BaseModel

__all__ = ['IncomingTextEvent', 'ErrorEvent']


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
