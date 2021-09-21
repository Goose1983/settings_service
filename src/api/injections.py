from logging import Logger
from typing import Generator

from src.core.data_source import engine

import logging


async def get_db() -> Generator:
    with engine.connect() as connection:
        yield connection


async def get_logger() -> Logger:
    return logging.getLogger("uvicorn.error")
