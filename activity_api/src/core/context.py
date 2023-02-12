"""Контекст для приложения."""
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar('request_id', default='')
