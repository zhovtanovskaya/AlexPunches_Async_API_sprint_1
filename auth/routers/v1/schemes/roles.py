from pydantic import BaseModel, PositiveInt, constr


class RoleBase(BaseModel):
    name: constr(max_length=80, strip_whitespace=True)
    description: str | None = None


class RoleCreate(RoleBase):
    pass


class RoleEdit(RoleBase):
    name: constr(max_length=80, strip_whitespace=True) | None = None
    description: str | None = None


class RoleScheme(RoleBase):
    id: PositiveInt

    class Config:
        orm_mode = True
