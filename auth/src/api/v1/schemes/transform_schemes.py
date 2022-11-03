"""Трансформация из пидантик-схем АПИ в пидантик-модели сервисов."""

from api.v1.schemes.login_histories import LoginHistoryCreateScheme
from services.models.login_histories import LoginHistoryCreateModel


def login_history_create_scheme_to_login_history_create_model(
        login_history_scheme: LoginHistoryCreateScheme,
        ) -> LoginHistoryCreateModel:
    """Трансформитровать LoginHistoryCreateScheme -> LoginHistoryCreateModel."""
    return LoginHistoryCreateModel(
        username=login_history_scheme.username,
        email=login_history_scheme.email,
        data_create=login_history_scheme.data_create,
        data_login=login_history_scheme.data_login,
    )
