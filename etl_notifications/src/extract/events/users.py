from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserSignedUpPayload(BaseModel):
    user_id: UUID | None
    email: EmailStr


class UserSignedUpEvent(BaseModel):
    id: UUID
    event_type: str = 'user_signed_up'
    priority: str = 'immediate'
    from_service: str = 'auth'
    details: UserSignedUpPayload

    class Config:
        orm_mode = True
