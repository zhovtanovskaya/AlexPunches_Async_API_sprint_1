from pydantic import BaseModel


class RoleScheme(BaseModel):
    """Роль."""

    id: int
    name: str
    description: str | None = None


class ListUserRolesScheme(BaseModel):
    """Список Ролей."""

    user_roles: list[RoleScheme] = []
