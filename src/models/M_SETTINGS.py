from sqlalchemy import MetaData, Table, Column

# Не использую тут ORM, так как он может подтормаживать. Фактически, SQLAlchemy используется в качестве query builder-а
from sqlalchemy.dialects.oracle import VARCHAR2, NUMBER

metadata = MetaData()

M_SETTINGS = Table(
    "M_SETTINGS",
    metadata,
    Column("key", VARCHAR2(50), primary_key=True),
    Column("value", VARCHAR2(100)),
    Column("description", VARCHAR2(256))
)
