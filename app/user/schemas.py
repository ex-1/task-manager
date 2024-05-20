from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserIn(UserSchema):
    name: str


class PassportUserPut(BaseModel):
    user_id: int
    passport_number: str
    issue_date: str
    expiration_date: str
    place_of_issue: str


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
