"""Трансформация из пидантик-схем АПИ в пидантик-модели сервисов."""

from api.v1.schemes.users import UserCreateScheme, UserEditScheme, LoginHistoryCreateScheme
from services.models.users import UserCreateModel, UserEditModel, LoginHistoryCreateModel


def user_create_scheme_to_user_create_model(user_scheme: UserCreateScheme,
                                            ) -> UserCreateModel:
    """Трансформитровать UserCreateScheme -> UserCreateModel."""
    return UserCreateModel(
        email=user_scheme.email,
        login=user_scheme.login,
        password=user_scheme.password,
    )


def user_edit_scheme_to_user_edit_model(user_scheme: UserEditScheme,
                                        ) -> UserEditModel:
    """Трансформитровать UserEditScheme -> UserEditModel."""
    return UserEditModel(
        email=user_scheme.email,
        login=user_scheme.login,
        password=user_scheme.password,


def login_history_create_scheme_to_login_history_create_model(
        login_history_scheme: LoginHistoryCreateScheme,
        ) -> LoginHistoryCreateModel:
    """Трансформитровать LoginHistoryCreateScheme ->
        LoginHistoryCreateModel."""
    return LoginHistoryCreateModel(
        username=login_history_scheme.username,
        email=login_history_scheme.email,
        data_create=login_history_scheme.data_create,
        data_login=login_history_scheme.data_login,)        
