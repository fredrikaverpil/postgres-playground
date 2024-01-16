import os  # noqa: INP001

import pytest
from playhouse.db_url import connect

DB = os.environ.get(
    "DB_CONN_POSTGRES",
    "postgres://postgres:secret@localhost:5400/postgres",
)


@pytest.fixture()
def peewee_db():  # noqa: ANN201
    # https://docs.peewee-orm.com/en/latest/peewee/database.html

    db = connect(DB)

    yield db

    with db.atomic():
        drop_schema = """
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;

            GRANT ALL ON SCHEMA public TO postgres;
            GRANT ALL ON SCHEMA public TO public;
        """
        db.execute_sql(drop_schema)

    db.close()


@pytest.fixture()
def peewee_query():  # noqa: ANN201
    def _peewee_query(db, sql, sql_params=None):  # noqa: ANN001, ANN202
        cursor = db.execute_sql(sql, sql_params)

        columns = [field_md[0] for field_md in cursor.description]
        rows = cursor.fetchall()

        return columns, rows

    return _peewee_query
