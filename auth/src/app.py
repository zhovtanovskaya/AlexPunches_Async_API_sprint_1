"""Создать фабрику для приложения."""
import sentry_sdk
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)
from sentry_sdk.integrations.flask import FlaskIntegration

from api.v1.auth import auth
from api.v1.login_histories import login_histories
from api.v1.profile import profile
from api.v1.roles import roles
from api.v1.users import users
from core.config import config
from core.db import db
from core.exceptions import exceptions


def configure_tracer() -> None:
    """Настроить трасировщик."""
    resource = Resource(attributes={
         SERVICE_NAME: config.project_name,
    })
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='localhost',
                agent_port=6831,
            ),
        ),
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter()),
    )


configure_tracer()


def create_app():
    """Фабрика приложения."""
    app = Flask(__name__)
    app.config.from_object(config.flask_config)
    app.register_blueprint(exceptions)
    app.register_blueprint(users, url_prefix='/api/v1')
    app.register_blueprint(roles, url_prefix='/api/v1')
    app.register_blueprint(auth, url_prefix='/api/v1')
    app.register_blueprint(login_histories, url_prefix='/api/v1')
    app.register_blueprint(profile, url_prefix='/api/v1')
    db.app = app
    db.init_app(app)
    if config.enable_tracer:
        FlaskInstrumentor().instrument_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)
    app.jwt = JWTManager(app)
    Limiter(
        app,
        key_func=get_remote_address,
        default_limits=['30 per second'],
        storage_uri=f'redis://{config.redis_host}:{config.redis_port}',
    )
    sentry_sdk.init(
        dsn=config.auth_sentry_dsn,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )
    return app




