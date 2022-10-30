
# Репозиторий
[https://github.com/AlexPunches/Async_API_sprint_1](https://github.com/AlexPunches/Async_API_sprint_1)

# Подготовка

В проекте используются переменные окружения. Они определяются несколькими  `.env`-файлами  
`.env` —   
`.env.dev` —   
`.env.pytests` —   

```bash
cp .env.sample .env
cp .env.sample .env.dev
cp .env.sample .env.pytests
```

# Запуск

Собрать и запустить контейнеры
```bash
make build
make up
```

Если нужно, переносим данные из SQLite в Postgres
```bash
make load-data
```

### Кеширование в Redis
Кешируем все GET-запросы по ключу `url`. Кешируемся на уровне `Middleware`.  
Кешируем с заголовками, в тч `date`. ¯\_(ツ)_/¯  
Если есть кеш, то ответ будет из кеша, и будет обозначее заголовком  `X-From-Redis-Cache: True`.  
Чтобы получить ответ минуя кеш, нужно передать заголовок `X-Not-Cache: True`  

### Потрогать
Админка  
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
OAS3  
[http://127.0.0.1:8000/api/openapi](http://127.0.0.1:8000/api/openapi)  


ETL Тесты
```bash
make etl-pytest
```

Остановить контейнеры
```bash
make stop
```

Остановить и удалить контейнеры, **и волюмы!**
```bash
make down
```

### На всякий случай
Запустить ETL из Postgres в Elasticsearch
```bash
make load-es-movies
```

В Makefile есть еще несколько полезных поманд, их можно подсмотреть в самом [Makefile](Makefile)

# Режим разработки 

Для сервисов `fastapi` или `etl`.  
Чтобы было удобно разрабатывать и дебажить будем запускать их в локальном виртуальном окружении.
А остальные через специальный `docker-compose.dev.yml`. В нем проброшены порты.  
Делается это просто:
```bash
make up-dev
```
При этом нужно проследить, чтобы у запускаемого сервиса были нужные переменные окружения.  
Например в Пайчарме это удобно сделать:  
в "Run/Debag Configurations -> EnvFile" указаваем предварительно созданный `.env.dev`,  
который нужным образом отличается от боевого, например, в нем хосты будут `localhost`, а `DEBUG` можно сделать `'True'`.  
Используем заготовочку
```bash
cp .env.sample .env.dev
```


_Для `admin_panel` режим разработки уже, наверно, неактуален._  
_Но если потребуется, нужно будет подкорректировать `docker-compose.dev.yml`_  

# Настройка разработки

```bash
pip install -r auth/requirements.dev.txt
pre-commit install
```

Вариант подключения [flake8 к PyCharm](https://melevir.medium.com/pycharm-loves-flake-671c7fac4f52).
Плагин [mypy для PyCharm](https://plugins.jetbrains.com/plugin/11086-mypy).
