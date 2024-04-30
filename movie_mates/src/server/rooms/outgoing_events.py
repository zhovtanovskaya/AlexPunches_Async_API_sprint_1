"""События, которые может посылать комната websocket-клиенту."""

from pydantic import BaseModel

__all__ = ['SetLeadingClientEvent']


class SetLeadingClientEvent(BaseModel):
    """Уведомление клиента о том, что он становится ведущим."""

    type: str = 'set_leading_client'
