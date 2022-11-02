"""Фикстуры-утилиты."""

import asyncio

import pytest


@pytest.fixture(scope='session')
def event_loop(request):
    """Фикстура с event_loop."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
