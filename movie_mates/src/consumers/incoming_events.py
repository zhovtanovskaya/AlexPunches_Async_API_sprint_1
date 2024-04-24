"""Входящие события от клиента серверу через вебсокет."""

from pydantic import BaseModel


class SendTextEvent(BaseModel):
    """Событие в веб-сокете.

    Например, сообщение от одного пользователя другому или
    запрос помощи в чате.
    """
    type: str
    to: str = ''
    text: str = ''


class SetUserNameEvent(BaseModel):
    """Собитие установки нового имени пользователя."""
    type: str = 'set_name'
    user_name: str
