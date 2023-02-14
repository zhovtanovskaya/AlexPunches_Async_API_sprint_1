
# Репозиторий
[https://github.com/AlexPunches/Async_API_sprint_1](https://github.com/AlexPunches/Async_API_sprint_1)

# Спринт 9

- [Бенчмаркинг Монги добавился к прошлым бенчмаркингам](https://github.com/AlexPunches/Async_API_sprint_1/blob/main/benchmarking_storage)
- [Структура проекта .plantuml](https://github.com/AlexPunches/Async_API_sprint_1/tree/main/documentation/architecture/sprint_9)
- [API для UGC подселился к activity_api](https://github.com/AlexPunches/Async_API_sprint_1/tree/main/activity_api)


# Подготовка проекта

В проекте используются переменные окружения. Они определяются несколькими  `.env`-файлами  
`.env`, `.env.dev`, `.env.pytests`  


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

### Потрогать
Админка  
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
OAS3  
[http://127.0.0.1:8000/api/openapi](http://127.0.0.1:8000/api/openapi)  

Остановить контейнеры
```bash
make stop
```

Остановить и удалить контейнеры, **и волюмы!**
```bash
make down
```


## Тесты

ETL Тесты
```bash
make etl-pytest
```
Async. FastAPI Тесты
```bash
make api-pytest
```
Auth Тесты
```bash
make auth-pytest
```

----

### На всякий случай
Запустить ETL из Postgres в Elasticsearch
```bash
make load-es-movies
```
Миграции для Auth
```bash
make auth-migrate
```

В Makefile есть еще несколько полезных поманд, их можно подсмотреть в самом [Makefile](Makefile)

### Кеширование FastAPI в Redis
Кешируем все GET-запросы по ключу `url`. Кешируемся на уровне `Middleware`.  
Кешируем с заголовками, в тч `date`. ¯\_(ツ)_/¯  
Если есть кеш, то ответ будет из кеша, и будет обозначее заголовком  `X-From-Redis-Cache: True`.  
Чтобы получить ответ минуя кеш, нужно передать заголовок `X-Not-Cache: True`  


# Режим разработки 

Для сервисов `etl`, `fastapi` или `Auth`.  
Чтобы было удобно разрабатывать и дебажить будем запускать их в локальном виртуальном окружении.
А остальные через специальный `docker-compose.dev.yml`. В нем проброшены порты.  
Делается это просто:
```bash
make up-dev
```
При этом нужно проследить, чтобы у запускаемого сервиса были нужные переменные окружения.  

*. например в Пайчарме это удобно сделать:
в "Run/Debag Configurations -> EnvFile" указаваем предварительно созданный `.env.dev`  
*. в терминале `export $(grep -v '^#' .env.dev | xargs)`  
или что-то типо
```bash
set -a
. .env.dev
```
и запускаем, 
```bash
python3.10 -m venv venv
source venv/bin/activate
```
Auth:
```bash
pip install -r ./auth/requirements.txt
python ./auth/src/manage.py db upgrade head  # если нужно накатить миграции
python ./auth/src/manage.py run
```
fastapi:
```bash
pip install -r ./fastapi/requirements.txt
python -m uvicorn main:app --reload --port $API_PORT --app-dir=./fastapi/src/
```
activity_api:
```bash
pip install -r ./activity_api/requirements.txt
python -m uvicorn main:app --reload --port $ACTIVITY_API_PORT --app-dir=./activity_api/src/
```
etl:
```bash
pip install -r ./etl_services/requirements.txt
cd ./etl_services
python sqlite_to_postgres/load_data.py
python postgres_to_es/load_indexes.py
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




____
# Миграции для Auth
При изменении структуры базы Auth не забыть создать и применить миграции.
Внутри контейнера или в виртуальном окружении:  
в контейнере:
```bash
# собрать миграции:
docker exec <CONTAINER_NAME_AUTH_FLASK> python src/manage.py db revision --message="<NAME_MIGRATION>" --autogenerate
# применить миграции:
docker exec <CONTAINER_NAME_AUTH_FLASK> python src/manage.py db upgrade head
```
в окружении:
```bash
# собрать миграции:
python src/manage.py db revision --message="<NAME_MIGRATION>" --autogenerate
# применить миграции:
python src/manage.py db upgrade head
```