import pytest
from websockets.sync.client import connect


@pytest.fixture(scope='session')
def ws_client():
    with connect('ws://localhost:8765/test_room/') as websocket:
        yield websocket
