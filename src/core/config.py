import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "ALFMATRIX settings"

    # Сервер
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "settings_server"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # База данных / Параметры подтягиваются из переменных окружения
    DATABASE_HOST: str = Field(..., env="DATABASE_HOST")
    DATABASE_PORT: str = Field(..., env="DATABASE_PORT")
    DATABASE_USER: str = Field(..., env="DATABASE_USER")
    DATABASE_PASSWORD: str = Field(..., env="DATABASE_PASSWORD")
    DATABASE_SERVICE_NAME: str = Field(..., env="DATABASE_SERVICE_NAME")
    DATABASE_POOL_SIZE: str = Field(..., env="DATABASE_POOL_SIZE")
    # DATABASE_HOST: str = "alfa-30"
    # DATABASE_PORT: str = "1521"
    # DATABASE_USER: str = "MTRX"
    # DATABASE_PASSWORD: str = "12345"
    # DATABASE_SERVICE_NAME: str = "cdb1"
    # DATABASE_POOL_SIZE: str = "10"
    SQLALCHEMY_DATABASE_URI: str = f"oracle+cx_oracle://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:" \
                                   f"{DATABASE_PORT}/?service_name={DATABASE_SERVICE_NAME} "

    # Путь к локальному клиенту
    # ORACLE_DIR: str = "C:/Program Files/Oracle/instantclient_12_2"  # for Windows local
    ORACLE_DIR: str = "/opt/oracle/instantclient_21_3"  # for Docker Conteiner

    # Логирование NOTSET = 0, DEBUG = 10, INFO = 20, WARNING = 30, ERROR = 40, FATAL = 50
    LOGGING_LEVEL: int = 10

settings = Settings()
