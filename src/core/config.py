import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "template_server"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "template_project"

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "55001"
    DATABASE_USER: str = "MATRIX"
    DATABASE_PASSWORD: str = "1234567890"
    DATABASE_SERVICE_NAME: str = "ORCLPDB1.localdomain"
    DATABASE_POOL_SIZE: str = "20"
    SQLALCHEMY_DATABASE_URI: str = f"oracle+cx_oracle://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/?service_name={DATABASE_SERVICE_NAME}"

    USERS_OPEN_REGISTRATION: bool = True

    class Config:
        env_prefix = ""
        env_file = ".env"
        case_sensitive = True


settings = Settings()
