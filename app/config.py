from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    P_DB: str
    P_USER: str
    P_PASS: str
    HOST: str
    PORT: int


settings = Settings()
