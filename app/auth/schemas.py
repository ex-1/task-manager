from datetime import datetime

from pydantic import BaseModel


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenIn(BaseModel):
    sub: str
    exp: datetime
