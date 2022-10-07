from pydantic import BaseModel, PositiveInt, constr


class RoleBase(BaseModel):
    name: constr(max_length=80, strip_whitespace=True)
    description: str | None = None


class RoleCreate(RoleBase):
    pass


class RoleScheme(RoleBase):
    id: PositiveInt
