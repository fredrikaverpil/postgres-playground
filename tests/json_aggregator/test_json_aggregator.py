import json  # noqa: D100
import pathlib


def test_export_json_data(  # noqa: ANN201, D103
    psycopg2_cursor, psycopg2_query, tmp_path  # noqa: ANN001
):  # noqa: ANN001, ANN201, D103, RUF100
    limit = 3

    psycopg2_cursor.execute(
        pathlib.Path(__file__).parent.joinpath("create_and_insert.sql").read_text(),
    )

    sql = pathlib.Path(__file__).parent.joinpath("export_json.sql").read_text()
    sql_params = (limit, limit)
    columns, rows = psycopg2_query(psycopg2_cursor, sql, sql_params)

    json_filepath = tmp_path / "export.json"
    with open(json_filepath, "w") as outfile:
        json.dump(rows[0][0], outfile)
    with open(json_filepath) as infile:
        loaded_json = json.load(infile)

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
    assert rows[0][0] == loaded_json
