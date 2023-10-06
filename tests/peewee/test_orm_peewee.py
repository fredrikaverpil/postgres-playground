import pathlib


def test_peewee_create_table(peewee_db):  # noqa: ANN001, ANN201
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("create.sql").read_text(),
        )

    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("insert.sql").read_text(),
        )

    cursor = peewee_db.execute_sql("SELECT * FROM persons")
    rows = cursor.fetchall()

    assert len(list(rows)) == 1
    assert rows[0] == (1, "John", "Doe", None, None)
