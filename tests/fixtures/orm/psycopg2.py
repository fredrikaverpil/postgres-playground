import os  # noqa: D100
from typing import Callable
from urllib.parse import urlparse

import pytest

import psycopg2

DB = os.environ.get(
    "DB_CONN_POSTGRES", "postgres://postgres:secret@localhost:5400/postgres"
)


@pytest.fixture()
def psycopg2_cursor():  # noqa: ANN201
    """Return psycopg2 cursor.

    Note:
    ----
        Use psycopg2_conn instead.
    """  # noqa: D213
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
def psycopg2_query():  # noqa: ANN201
    """Return rows, columns from a query.

    Note:
    ----
        Use psycopg2_execute instead.
    """  # noqa: D213

    def _(cursor, sql, sql_params=None):  # noqa: ANN001, ANN202
        cursor.execute(sql, sql_params)
        columns = [field_md[0] for field_md in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    return _


@pytest.fixture()
def psycopg2_conn():  # noqa: ANN201, D103

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

    yield conn

    drop_schema = """
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;

        GRANT ALL ON SCHEMA public TO postgres;
        GRANT ALL ON SCHEMA public TO public;
    """
    cursor = conn.cursor()
    cursor.execute(drop_schema)
    cursor.close()
    conn.close()


@pytest.fixture()
def psycopg2_execute(psycopg2_conn) -> Callable:  # noqa: ANN001, D103
    def _(sql, sql_params=None, commit=False):  # noqa: ANN001, ANN202, FBT002
        cursor = psycopg2_conn.cursor()
        cursor.execute(sql, sql_params)
        if commit:
            psycopg2_conn.commit()
        return cursor

    return _


@pytest.fixture()
def psycopg2_columns() -> Callable:  # noqa: D103
    def _(cursor) -> list[str]:  # noqa: ANN001
        return [field_md[0] for field_md in cursor.description]

    return _
