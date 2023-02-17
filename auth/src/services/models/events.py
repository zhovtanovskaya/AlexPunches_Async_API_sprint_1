from uuid import UUID

from pydantic import BaseModel


class WelcomUserEventModel(BaseModel):
    id: UUID
    event_type: str = 'user_signed_up'
    priority: str = 'immediate'
    from_service: str = 'auth'
    details: dict

    class Config:  # noqa
        orm_mode = True
