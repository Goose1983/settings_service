from sqlalchemy import MetaData, Table, Column

# Не использую тут ORM, так как он может подтормаживать. Фактически, SQLAlchemy используется в качестве query builder-а
from sqlalchemy.dialects.oracle import VARCHAR2

metadata = MetaData()

M_REQUEST_PARAMETERS = Table(
    "M_REQUEST_PARAMETERS",
    metadata,
    Column("product_type", VARCHAR2(10)),
    Column("column_name", VARCHAR2(50)),
    Column("parameter_code", VARCHAR2(20))
)
