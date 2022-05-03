import os
from urllib.parse import urlparse

import psycopg2
import pytest

DB = os.environ.get(
    "DB_CONN_POSTGRES", "postgres://postgres:secret@localhost:5400/postgres"
)


@pytest.fixture()
def psycopg2_cursor():
    # ...

    uri = urlparse(DB)

    username = uri.username
    password = uri.password
    database = uri.path[1:]
    hostname = uri.hostname
    port = uri.port

    conn = psycopg2.connect(
        user=username,
        password=password,
        host=hostname,
        port=port,
        dbname=database,
    )

    cursor = conn.cursor()

    yield cursor

    drop_schema = """
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;

        GRANT ALL ON SCHEMA public TO postgres;
        GRANT ALL ON SCHEMA public TO public;
    """
    cursor.execute(drop_schema)

    conn.close()


@pytest.fixture()
def psycopg2_query():
    def _psycopg2_query(cursor, sql, sql_params=None):
        cursor.execute(sql, sql_params)
        columns = [field_md[0] for field_md in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    return _psycopg2_query
