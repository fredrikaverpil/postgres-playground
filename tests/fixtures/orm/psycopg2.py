import os
from typing import Callable
from urllib.parse import urlparse

import pytest

import psycopg2

DB = os.environ.get(
    "DB_CONN_POSTGRES", "postgres://postgres:secret@localhost:5400/postgres"
)


@pytest.fixture()
def psycopg2_cursor():
    """Return psycopg2 cursor.

    Note:
        Use psycopg2_conn instead.
    """

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
    """Return rows, columns from a query.

    Note:
        Use psycopg2_execute instead.
    """

    def _(cursor, sql, sql_params=None):
        cursor.execute(sql, sql_params)
        columns = [field_md[0] for field_md in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    return _


@pytest.fixture()
def psycopg2_conn():

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
def psycopg2_execute(psycopg2_conn) -> Callable:
    def _(sql, sql_params=None, commit=False):  # noqa: FBT002
        cursor = psycopg2_conn.cursor()
        cursor.execute(sql, sql_params)
        if commit:
            psycopg2_conn.commit()
        return cursor

    return _


@pytest.fixture()
def psycopg2_columns() -> Callable:
    def _(cursor) -> list[str]:
        return [field_md[0] for field_md in cursor.description]

    return _
