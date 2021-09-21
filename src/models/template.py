from sqlalchemy import MetaData, Table, Column

# Не использую тут ORM, так как он может подтормаживать. Фактически, SQLAlchemy используется в качестве query builder-а
from sqlalchemy.dialects.oracle import VARCHAR2, NUMBER

metadata = MetaData()

template = Table(
    "TEMPLATE",
    metadata,
    Column("ID", VARCHAR2(32), primary_key=True),
    Column("NAME", VARCHAR2(100), primary_key=True),
    Column("VALUE", VARCHAR2(100), primary_key=True),
    Column("VERSION", NUMBER(38,0), primary_key=True),
)