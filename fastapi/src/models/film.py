import orjson
from models import orjson_dumps
from pydantic import BaseModel


class Film(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
