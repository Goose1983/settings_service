from sqlalchemy import MetaData, Table, Column

# Не использую тут ORM, так как он может подтормаживать. Фактически, SQLAlchemy используется в качестве query builder-а
from sqlalchemy.dialects.oracle import TIMESTAMP, VARCHAR2

metadata = MetaData()

M_SETTINGS_DATE = Table(
    "M_SETTINGS_DATE",
    metadata,
    Column("table_name", VARCHAR2(30), primary_key=True),
    Column("sdate", TIMESTAMP),
)
