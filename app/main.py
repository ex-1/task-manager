from fastapi import FastAPI

from app.user.router import user

app = FastAPI()

app.include_router(user, prefix='/api/v1/user')


@app.get("/")
def read_root():
    return {"message": "Hello World"}
