from pydantic import BaseModel


class IncomingTextEvent(BaseModel):
    type: str = "incoming_text"
    author: str
    text: str


class ErrorEvent(BaseModel):
    type: str = "error"
    text: str
    on_event: str|dict