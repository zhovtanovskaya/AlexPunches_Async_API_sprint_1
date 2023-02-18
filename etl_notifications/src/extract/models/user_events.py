from pydantic import BaseModel


class UserCreatedEvent(BaseModel):
    text: str
