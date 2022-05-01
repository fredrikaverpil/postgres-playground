import pathlib

import pytest


@pytest.fixture()
def _create_cities_table(peewee_db):
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("003_create.sql").read_text()
        )
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("005_insert.sql").read_text()
        )


@pytest.mark.usefixtures("_create_cities_table")
def test_comparison_operator(peewee_db, peewee_query):
    """Test comparison operator.

    Available operators:
    - Eqality: =
    - Greater than: >
    - Less than: <
    - Greater or equal to: >=
    - Less or equal to: <=
    - Non-equal values: <> or !=
    - Value in list: IN
    - Value not in list: NOT IN
    - Value between two values: BETWEEN

    """
    expected_columns = ["name", "area"]
    expected_rows = [("Tokyo", 8223), ("Shanghai", 4015)]

    columns, rows = peewee_query(
        db=peewee_db,
        query=pathlib.Path(__file__).parent.joinpath("013a_select.sql").read_text(),
    )

    assert columns == expected_columns
    assert rows == expected_rows


@pytest.mark.usefixtures("_create_cities_table")
def test_calculation_in_where(peewee_db, peewee_query):
    expected_columns = ["name", "population_density"]
    expected_rows = [("Delhi", 12555), ("Sao Paulo", 6879)]

    columns, rows = peewee_query(
        db=peewee_db,
        query=pathlib.Path(__file__).parent.joinpath("013b_select.sql").read_text(),
    )

    assert columns == expected_columns
    assert rows == expected_rows


@pytest.mark.usefixtures("_create_cities_table")
def test_update(peewee_db, peewee_query):
    expected_columns = ["name", "country", "population", "area"]
    expected_rows = [
        ("Delhi", "India", 28125000, 2240),
        ("Shanghai", "China", 22125000, 4015),
        ("Sao Paulo", "Brazil", 20935000, 3043),
        ("Tokyo", "Japan", 39505000, 8223),
    ]

    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("022_update.sql").read_text()
        )

    columns, rows = peewee_query(
        db=peewee_db,
        query="SELECT * FROM cities",
    )

    assert columns == expected_columns
    assert rows == expected_rows


@pytest.mark.usefixtures("_create_cities_table")
def test_delete(peewee_db, peewee_query):
    expected_columns = ["name", "country", "population", "area"]
    expected_rows = [
        ("Delhi", "India", 28125000, 2240),
        ("Shanghai", "China", 22125000, 4015),
        ("Sao Paulo", "Brazil", 20935000, 3043),
    ]

    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("023_delete.sql").read_text()
        )

    columns, rows = peewee_query(
        db=peewee_db,
        query="SELECT * FROM cities",
    )

    assert columns == expected_columns
    assert rows == expected_rows
