from typing import Optional
from uuid import UUID

import orjson
from pydantic import BaseModel

from models import orjson_dumps


class Genre(BaseModel):
    id: UUID
    name: str
    description: Optional[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
