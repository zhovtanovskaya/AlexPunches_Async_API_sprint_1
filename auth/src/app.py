"""Создать фабрику для приложения."""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)

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
    trace.set_tracer_provider(TracerProvider())
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
    app.jwt = JWTManager(app)
    FlaskInstrumentor().instrument_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    return app
