from typing import Optional

from pydantic import BaseModel


class Event(BaseModel):
    """Событие в веб-сокете.

    Например, сообщение от одного пользователя другому или
    запрос помощи в чате.
    """
    type: str
    to: Optional[str] = ''
    content: str = ''
