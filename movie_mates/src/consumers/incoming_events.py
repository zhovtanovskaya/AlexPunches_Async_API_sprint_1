from typing import Optional

from pydantic import BaseModel


class SendTextEvent(BaseModel):
    """Событие в веб-сокете.

    Например, сообщение от одного пользователя другому или
    запрос помощи в чате.
    """
    type: str
    to: Optional[str] = ''
    text: str = ''


class SetUserNameEvent(BaseModel):
    type: str = 'set_name'
    user_name: str
