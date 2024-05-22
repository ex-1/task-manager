from datetime import date

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserIn(UserSchema):
    name: str


class PassportUserPut(BaseModel):
    passport_number: str | None = None
    issue_date: date | None = None
    expiration_date: date | None = None
    place_of_issue: str | None = None


class UserPut(BaseModel):
    username: str
    name: str
    passport_data: PassportUserPut


class UserOut(BaseModel):
    username: str
    id: int
    name: str


class UserOutWithPassword(UserOut):
    hashed_password: str


class CreatedUserMessage(BaseModel):
    result: str = "User Created"
