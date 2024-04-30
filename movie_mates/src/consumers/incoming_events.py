"""Входящие события от клиента серверу через вебсокет."""

from pydantic import BaseModel

__all__ = ['SendTextEvent', 'SetUserNameEvent', 'LeadingPlayerChangedEvent']


class SendTextEvent(BaseModel):
    """Событие в веб-сокете.

    Например, сообщение от одного пользователя другому или
    запрос помощи в чате.
    """

    type: str = 'send_text'
    to: str = ''
    text: str = ''


class SetUserNameEvent(BaseModel):
    """Собитие установки нового имени пользователя."""

    type: str = 'set_name'
    user_name: str


class LeadingPlayerChangedEvent(BaseModel):
    """Измененилось состояние ведущего плеера."""

    type: str = 'leading_player_changed'
    timecode: float
    player_status: str = 'play'
