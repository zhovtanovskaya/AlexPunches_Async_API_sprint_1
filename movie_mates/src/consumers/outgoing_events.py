from pydantic import BaseModel


class IncomingTextEvent(BaseModel):
    type: str = "incoming_text"
    author: str
    text: str