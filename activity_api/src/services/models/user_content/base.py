"""Сущности, общие для всех моделей пользовательского контента."""
from enum import Enum

from bson import ObjectId


class StrObjectId(ObjectId):
    """Класс для приведения строки к типу ObjecId."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId.')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class ContentType(str, Enum):
    """Типы пользовательского контента в Mongo."""

    MOVIE = 'movie'
    REVIEW = 'review'
    BOOKMARK = 'bookmark'
    RATING = 'rating'
    LIKE = 'like'
