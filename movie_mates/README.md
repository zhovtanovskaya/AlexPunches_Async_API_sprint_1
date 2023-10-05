## Movie Mates

WebSocket-сервер запускается командой `make run_server`.  Подключиться к нему можно
командой `websocat ws://localhost:8765`.  Примеры JSON-сообщений, которые можно слать
в комнату с двумя участниками Alison и Bob:
```
> {"type": "help", "content": "?"}
Alison, Bob
> {"type": "send_text", "content": "Alison: Hello!"}
```