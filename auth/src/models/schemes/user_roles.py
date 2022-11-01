from pydantic import BaseModel


class UserRoleCreateScheme(BaseModel):
    """Использовать при добавлении Юзер-Роли."""

    name: str
