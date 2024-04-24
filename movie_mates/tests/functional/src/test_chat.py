def test_clients_in_room(ws_client):
    ws_client.send('{"type": "help", "content": "?"}')
    message = ws_client.recv()
    assert message == 'AnonymousClient'


def test_set_client_name(ws_client):
    ws_client.send('{"type": "set_user_name", "user_name": "test_user"}')
    ws_client.send('{"type": "help", "content": "?"}')
    message = ws_client.recv()
    assert message == 'test_user'


def test_send_text_to_all(ws_client):
    ws_client.send('{"type": "send_text", "text": "Hello!", "to": "__all__"}')
    message = ws_client.recv()
    expected = '{"type":"incoming_text","author":"test_user","text":"Hello!"}'
    assert message == expected
    

def test_send_text_to_self(ws_client):
    ws_client.send('{"type": "send_text", "text": "Hello!", "to": "test_user"}')
    message = ws_client.recv()
    expected = '{"type":"incoming_text","author":"test_user","text":"Hello!"}'
    assert message == expected


def test_send_to_unknown_user(ws_client):
    ws_client.send('{"type": "send_text", "text": "Hello!", "to": "unknown_user"}')
    message = ws_client.recv()
    expected = (
        '{'
            '"type":"error",'
            '"text":"Пользователь unknown_user не найден",'
            '"on_event":{"type":"send_text","to":"unknown_user","text":"Hello!"}'
        '}'
    )
    assert message == expected
