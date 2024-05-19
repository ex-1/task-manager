from typing import Annotated

from fastapi import FastAPI, Depends, APIRouter

from app.auth.router import auth_router
from app.auth.services import get_current_user
from app.user.router import user_router
from app.user.schemas import UserOut

app = FastAPI()
services = APIRouter(prefix="/api")
services.include_router(user_router)
services.include_router(auth_router)
app.include_router(services)


@app.get("/")
def core(current_user: Annotated[UserOut, Depends(get_current_user)]) -> dict[str, str]:
    return {"hello": "world"}
