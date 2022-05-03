import pathlib


def test_export_data(psycopg2_cursor, psycopg2_query):

    psycopg2_cursor.execute(
        pathlib.Path(__file__).parent.joinpath("create_and_insert.sql").read_text(),
    )

    sql = pathlib.Path(__file__).parent.joinpath("export.sql").read_text()
    columns, rows = psycopg2_query(psycopg2_cursor, sql)

    assert columns == ["json_agg"]
    assert rows == [
        (
            [
                {"url": "http://36.jpg", "user_id": 1, "username": "monahan93"},
                {"url": "http://25.jpg", "user_id": 1, "username": "monahan93"},
                {"url": "http://two.jpg", "user_id": 1, "username": "monahan93"},
                {"url": "http://754.jpg", "user_id": 2, "username": "pferrer"},
                {"url": "http://35.jpg", "user_id": 3, "username": "si93onis"},
                {"url": "http://256.jpg", "user_id": 4, "username": "99stroman"},
                {"url": "http://one.jpg", "user_id": 4, "username": "99stroman"},
            ],
        ),
    ]
