"""
/api/v1/genres/
/api/v1/genres/<uuid:UUID>/
"""
from http import HTTPStatus
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from services.film import FilmService, get_film_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


class Genre(BaseModel):
    id: UUID = Field(..., alias='uuid')
    name: str

    class Config:
        allow_population_by_field_name = True
