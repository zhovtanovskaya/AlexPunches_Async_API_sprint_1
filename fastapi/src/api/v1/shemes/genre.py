from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GenreShort(BaseModel):
    id: UUID = Field(..., alias='uuid')
    name: str

    class Config:
        allow_population_by_field_name = True


class Genre(GenreShort):
    description: Optional[str]
