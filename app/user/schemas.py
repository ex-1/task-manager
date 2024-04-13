from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str


class UserIn(UserSchema):
    password: str


class UserOut(UserSchema):
    id: int

    class Config:
        orm_mode = True
