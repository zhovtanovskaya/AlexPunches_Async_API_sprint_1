"""Трансформация из пидантик-схем АПИ в пидантик-модели сервисов.

В трансформациях аннотированы Родительские пидантик схемы и модели,
т.к. в них все возможные поля и они необязательные.
"""

import api.v1.schemes.roles as role_schemes
import api.v1.schemes.users as user_schemes
import services.models.roles as service_role_models
import services.models.users as service_user_models


def user_scheme_to_user_model(
          user_scheme: user_schemes.UserBaseScheme,
) -> service_user_models.UserBaseModel:
    """Трансформитровать UserScheme -> UserModel.

    Поисходит через dict() схемы,
    чтобы сделать exclude_unset и не добавлять unset в итоговую модель.
    """
    exc_unset_dict = user_scheme.dict(exclude_unset=True)
    user_model = service_user_models.UserBaseModel()
    if 'id' in exc_unset_dict:
        user_model.id = exc_unset_dict['id']
    if 'email' in exc_unset_dict:
        user_model.email = exc_unset_dict['email']
    if 'login' in exc_unset_dict:
        user_model.login = exc_unset_dict['login']
    if 'active' in exc_unset_dict:
        user_model.active = exc_unset_dict['active']
    if 'roles' in exc_unset_dict:
        user_model.roles = exc_unset_dict['roles']
    if 'password' in exc_unset_dict:
        user_model.password = exc_unset_dict['password']
    return user_model


def user_model_to_user_scheme(
          user_model: service_user_models.UserBaseModel,
) -> user_schemes.UserScheme:
    """Трансформитровать UserModel -> UserScheme."""
    return user_schemes.UserScheme(
        id=user_model.id,
        email=user_model.email,
        login=user_model.login,
        active=user_model.active,
        roles=user_model.roles,
    )


def role_scheme_to_role_model(
          role_scheme: role_schemes.RoleBaseScheme,
) -> service_role_models.RoleBaseModel:
    """Трансформировать RoleScheme -> RoleModel."""
    return service_role_models.RoleBaseModel(
        id=role_scheme.id,
        name=role_scheme.name,
        description=role_scheme.description,
    )


def role_model_to_role_scheme(
          role_model: service_role_models.RoleBaseModel,
) -> role_schemes.RoleBaseScheme:
    """Трансформировать RoleModel -> RoleScheme."""
    return role_schemes.RoleBaseScheme(
        id=role_model.id,
        name=role_model.name,
        description=role_model.description,
    )
