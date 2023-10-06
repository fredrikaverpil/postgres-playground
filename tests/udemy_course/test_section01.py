import pathlib

import pytest


@pytest.fixture()
def _create_cities_table(peewee_db):  # noqa: ANN001, ANN202
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("003_create.sql").read_text(),
        )


@pytest.mark.usefixtures("_create_cities_table")
def test_insert(peewee_db):  # noqa: ANN001, ANN201
    expected = [
        ("Tokyo", "Japan", 38505000, 8223),
        ("Delhi", "India", 28125000, 2240),
        ("Shanghai", "China", 22125000, 4015),
        ("Sao Paulo", "Brazil", 20935000, 3043),
    ]

    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("005_insert.sql").read_text(),
        )

    cursor = peewee_db.execute_sql("SELECT * FROM cities")
    rows = cursor.fetchall()

    tables = peewee_db.get_tables()

    assert rows == expected
    assert tables == ["cities"]


@pytest.mark.usefixtures("_create_cities_table")
def test_calculation(peewee_db, peewee_query):  # noqa: ANN001, ANN201
    """Test calculation.

    Available operators:
    - Add: +
    - Subtract: -
    - Multiply: *
    - Divide: /
    - Exponent: ^
    - Square root: |/
    - Absolute value: @
    - Remainder: %
    """
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("005_insert.sql").read_text(),
        )
    columns, rows = peewee_query(
        db=peewee_db,
        sql="""SELECT name, population / area AS population_density FROM cities""",
    )

    expected_columns = ["name", "population_density"]
    expected_rows = [
        ("Tokyo", 4682),
        ("Delhi", 12555),
        ("Shanghai", 5510),
        ("Sao Paulo", 6879),
    ]
    assert columns == expected_columns
    assert rows == expected_rows


@pytest.mark.usefixtures("_create_cities_table")
def test_string_operators_and_functions(  # noqa: ANN201
    peewee_db,  # noqa: ANN001
    peewee_query,  # noqa: ANN001
):  # noqa: ANN001, ANN201, RUF100
    """Test calculation.

    Available operators:
    - Join two strings: ||
    - Joint two strings: CONCAT()
    - Give lower case string: LOWER()
    - Give number of characters in string: LENGTH()
    - Give upper case string: UPPER()
    """
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("005_insert.sql").read_text(),
        )
    columns, rows = peewee_query(
        db=peewee_db,
        sql="""
        SELECT name || ', ' || country AS "location"
          FROM cities
        """,
    )
    columns2, rows2 = peewee_query(
        db=peewee_db,
        sql="""
        SELECT CONCAT(name, ', ', country) AS "location"
          FROM cities
        """,
    )

    expected_columns = ["location"]
    expected_rows = [
        ("Tokyo, Japan",),
        ("Delhi, India",),
        ("Shanghai, China",),
        ("Sao Paulo, Brazil",),
    ]
    assert columns == columns2 == expected_columns
    assert rows == rows2 == expected_rows
