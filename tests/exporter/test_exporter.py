import pathlib


def test_export_data(psycopg2_cursor, psycopg2_query):
    limit = 3

    psycopg2_cursor.execute(
        pathlib.Path(__file__).parent.joinpath("create_and_insert.sql").read_text(),
    )

    sql = pathlib.Path(__file__).parent.joinpath("export.sql").read_text()
    sql_params = (limit, limit)
    columns, rows = psycopg2_query(psycopg2_cursor, sql, sql_params)

    assert columns == ["json_agg"]
    assert rows == [
        (
            [
                {"url": "http://one.jpg", "username": "99stroman"},
                {"url": "http://two.jpg", "username": "monahan93"},
                {"url": "http://25.jpg", "username": "monahan93"},
            ],
        )
    ]
