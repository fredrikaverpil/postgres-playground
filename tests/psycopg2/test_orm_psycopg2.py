import pathlib


def test_psycopg2_cursor(psycopg2_cursor):
    psycopg2_cursor.execute(
        pathlib.Path(__file__).parent.joinpath("create.sql").read_text(),
    )

    psycopg2_cursor.execute(
        pathlib.Path(__file__).parent.joinpath("insert.sql").read_text(),
    )

    psycopg2_cursor.execute("SELECT * FROM persons")
    rows = psycopg2_cursor.fetchall()

    assert len(list(rows)) == 1
    assert rows[0] == (1, "John", "Doe", None, None)


def test_psycopg2_query(psycopg2_cursor, psycopg2_query):
    psycopg2_cursor.execute(
        pathlib.Path(__file__).parent.joinpath("create.sql").read_text(),
    )

    psycopg2_cursor.execute(
        pathlib.Path(__file__).parent.joinpath("insert.sql").read_text(),
    )

    columns, rows = psycopg2_query(psycopg2_cursor, "SELECT * FROM persons")

    assert columns == ["id", "first_name", "last_name", "address", "city"]
    assert rows == [(1, "John", "Doe", None, None)]
