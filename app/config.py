from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    P_USER: str
    P_PASS: str
    P_DB: str
    P_HOST: str
    P_DRIVER: str
    P_ASYNC_DRIVER: str
    P_PORT: int

    # auth
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = PostgresSettings()
