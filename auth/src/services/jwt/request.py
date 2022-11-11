"""Утилиты для работы с JWT из запроса."""

from flask_jwt_extended import get_jwt, jwt_required

__all__ = ['get_jwt', 'jwt_required']
