from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import auth_router
from app.task.router import project_router, task_router
from app.user.router import user_router

app = FastAPI()
services = APIRouter(prefix="/api")
services.include_router(user_router)
services.include_router(auth_router)
services.include_router(project_router)
services.include_router(task_router)
app.include_router(services)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)