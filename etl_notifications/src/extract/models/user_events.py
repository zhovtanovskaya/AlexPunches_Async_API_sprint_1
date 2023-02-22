from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreatedEvent(BaseModel):
    user_id: UUID
    user_email: EmailStr
