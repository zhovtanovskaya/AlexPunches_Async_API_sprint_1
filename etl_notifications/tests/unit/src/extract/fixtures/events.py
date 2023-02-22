from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserSignedUpPayload(BaseModel):
    user_id: UUID = '0ebc9f39-d195-4051-9df8-263db5e6962b'
    email: EmailStr = 'user@mail.com'


class UserSignedUpEvent(BaseModel):
    id: UUID = '54006f75-728d-464b-aa51-b42021388ed1'
    event_type: str = 'user_signed_up'
    priority: str = 'immediate'
    from_service: str = 'auth'
    details: UserSignedUpPayload = UserSignedUpPayload()
