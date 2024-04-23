def test_clients_in_room(ws_client):
    ws_client.send('{"type": "help", "content": "?"}')
    message = ws_client.recv()
    assert message == 'AnonymousClient'


def test_set_client_name(ws_client):
    ws_client.send('{"type": "set_user_name", "user_name": "test_user"}')
    ws_client.send('{"type": "help", "content": "?"}')
    message = ws_client.recv()
    assert message == 'test_user'