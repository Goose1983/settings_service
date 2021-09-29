import cx_Oracle
from sqlalchemy import create_engine

from src.core.config import settings

# Вот тут нужно подложить свою директорию до ораклового клиента
# Потом тут будет статическая строчка с директорией до ораклового клиента внутри контейнера
cx_Oracle.init_oracle_client(lib_dir=settings.ORACLE_DIR)

SQLALCHEMY_DATABASE_URI: str = f"oracle+cx_oracle://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@" \
                               f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}" \
                               f"/?service_name={settings.DATABASE_SERVICE_NAME}"

# Грустно, но официального асинхронного клиента к Oracle нет, поэтому используем синхронный.
# Делать multithread-обвязку, имхо, слишком дорого сейчас
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=int(settings.DATABASE_POOL_SIZE))
