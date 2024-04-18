from pydantic import BaseModel


class UserSchema(BaseModel):
    user: str
    email: str


class UserIn(UserSchema):
    password: str


class UserOut(UserSchema):
    id: int

    class Config:
        orm_mode = True
