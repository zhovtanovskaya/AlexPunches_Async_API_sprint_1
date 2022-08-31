build:
	docker-compose -f ./docker-compose.yml build
up:
	docker-compose -f ./docker-compose.yml up -d
createsuperuser:
	docker-compose -f ./docker-compose.yml exec admin_panel python manage.py createsuperuser
makemigrations:
	docker-compose -f ./docker-compose.yml exec admin_panel python manage.py makemigrations
migrate:
	docker-compose -f ./docker-compose.yml exec admin_panel python manage.py migrate
load-data:
	docker-compose -f ./docker-compose.yml run etl python sqlite_to_postgres/load_data.py
etl-pytest:
	docker-compose -f ./docker-compose.yml run etl pytest -v
stop:
	docker-compose -f ./docker-compose.yml stop
down:
	docker-compose -f ./docker-compose.yml down -v
logs:
	docker-compose -f ./docker-compose.yml logs -f
load-es-movies:
	docker-compose -f ./docker-compose.yml run etl python postgres_to_es/load_indexes.py
up-dev:
	docker-compose -f ./docker-compose.dev.yml up -d
api-pytest:
	docker-compose -f ./fastapi/tests/functional/docker-compose.yml up -d --build
	docker-compose -f ./fastapi/tests/functional/docker-compose.yml logs -f pytests