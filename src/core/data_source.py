import cx_Oracle
from sqlalchemy import create_engine

from src.core.config import settings

# Вот тут нужно подложить свою директорию до ораклового клиента
# Потом тут будет статическая строчка с директорией до ораклового клиента внутри контейнера
cx_Oracle.init_oracle_client()

# Грустно, но официального асинхронного клиента к Oracle нет, поэтому используем синхронный.
# Делать multithread-обвязку, имхо, слишком дорого сейчас
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_size=int(settings.DATABASE_POOL_SIZE))
