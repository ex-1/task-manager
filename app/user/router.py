from fastapi import APIRouter


user = APIRouter(prefix='user')


@user.get("/")
def root():
    pass
