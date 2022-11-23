build:
	docker-compose -f ./docker-compose.yml --env-file .env build
up:
	docker-compose -f ./docker-compose.yml --env-file .env up -d
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
	docker-compose -f ./docker-compose.dev.yml stop
	docker-compose -f ./fastapi/tests/functional/docker-compose.yml stop
	docker-compose -f ./auth/tests/functional/docker-compose.yml stop
down:
	docker-compose -f ./docker-compose.yml down -v
	docker-compose -f ./docker-compose.dev.yml down -v
	docker-compose -f ./fastapi/tests/functional/docker-compose.yml down -v
	docker-compose -f ./auth/tests/functional/docker-compose.yml down -v
logs:
	docker-compose -f ./docker-compose.yml logs -f
load-es-movies:
	docker-compose -f ./docker-compose.yml run etl python postgres_to_es/load_indexes.py
up-dev:
	docker-compose -f ./docker-compose.dev.yml --env-file .env.dev up -d
api-pytest:
	docker-compose -f ./fastapi/tests/functional/docker-compose.yml --env-file .env.pytests up -d --build
	docker-compose -f ./fastapi/tests/functional/docker-compose.yml logs -f pytests
auth-pytest:
	docker-compose -f ./auth/tests/functional/docker-compose.yml --env-file .env.pytests up -d --build
	docker-compose -f ./auth/tests/functional/docker-compose.yml logs -f auth-pytests
auth-migrate:
	docker-compose -f ./docker-compose.yml exec auth_flask python src/manage.py db upgrade head

env:
	cp .env.sample .env
	cp .env.sample .env.dev
	sed -i "s/DB_HOST_ADMIN=.*/DB_HOST_ADMIN=localhost/"  .env.dev
	sed -i "s/DB_PORT_ADMIN=.*/DB_PORT_ADMIN=15432/"  .env.dev
	sed -i "s/ES_HOST=.*/ES_HOST=localhost/"  .env.dev
	sed -i "s/USE_CACHE=.*/USE_CACHE=False/"  .env.dev
	sed -i "s/REDIS_HOST=.*/REDIS_HOST=localhost/"  .env.dev
	sed -i "s/API_HOST=.*/API_HOST=localhost/"  .env.dev
	sed -i "s/API_PORT=.*/API_PORT=8001/"  .env.dev
	sed -i "s/OAUTHLIB_INSECURE_TRANSPORT=.*/OAUTHLIB_INSECURE_TRANSPORT=1/"  .env.dev
	sed -i "s/GOOGLE_OAUTH_ENDPOINT=.*/GOOGLE_OAUTH_ENDPOINT=http\:\/\/localhost\:5000\/api\/v1\/social-auth\/google/"  .env.dev
	sed -i "s/ENABLE_TRACER=.*/ENABLE_TRACER=False/"  .env.dev
	sed -i "s/JAEGER_HOST=.*/JAEGER_HOST=localhost/"  .env.dev
	sed -i "s/DB_HOST_AUTH=.*/DB_HOST_AUTH=localhost/"  .env.dev
	cp .env.sample .env.pytests
	sed -i "s/ES_HOST=.*/ES_HOST=test-elastic/" .env.pytests
	sed -i "s/REDIS_HOST=.*/REDIS_HOST=test-redis/" .env.pytests
	sed -i "s/API_HOST=.*/API_HOST=test-fastapi/" .env.pytests
	sed -i "s/ENABLE_TRACER=.*/ENABLE_TRACER=False/" .env.pytests
	sed -i "s/OAUTHLIB_INSECURE_TRANSPORT=.*/OAUTHLIB_INSECURE_TRANSPORT=1/"  .env.pytests
	sed -i "s/JAEGER_HOST=.*/JAEGER_HOST=jaeger/" .env.pytests
	sed -i "s/DB_HOST_AUTH=.*/DB_HOST_AUTH=test-auth-postgres/" .env.pytests
