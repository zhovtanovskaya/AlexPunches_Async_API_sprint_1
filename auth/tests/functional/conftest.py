"""Фикстуры."""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


pytest_plugins = [
    'functional.fixtures.data',
    'functional.fixtures.clients',
    'functional.fixtures.utils',
]
