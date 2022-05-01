import pathlib


def test_peewee_create_table(peewee_db):
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("create.sql").read_text()
        )
