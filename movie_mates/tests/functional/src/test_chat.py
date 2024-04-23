def test(ws_client):
    ws_client.send('{"type": "help", "content": "?"}')
    message = ws_client.recv()
    assert message == 'AnonymousClient'