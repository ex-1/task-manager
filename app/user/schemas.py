from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserIn(UserSchema):
    email: str


class UserOut(BaseModel):
    username: str
    id: int
    email: str


class UserOutWithPassword(UserOut):
    hashed_password: str


class CreatedUserMessage(BaseModel):
    result: str = "User Created"
