import pathlib  # noqa: D100

import pytest

import peewee


@pytest.fixture()
def _create_users_table(peewee_db):  # noqa: ANN001, ANN202
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("028a_create.sql").read_text()
        )
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("028b_insert.sql").read_text()
        )


@pytest.fixture()
def _create_photos_table(peewee_db):  # noqa: ANN001, ANN202
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("028c_create.sql").read_text()
        )
    with peewee_db.atomic():
        peewee_db.execute_sql(
            pathlib.Path(__file__).parent.joinpath("028d_insert.sql").read_text()
        )


@pytest.mark.usefixtures("_create_users_table", "_create_photos_table")
def test_select_with_join(peewee_db, peewee_query):  # noqa: ANN001, ANN201, D103
    expected_columns = ["url", "username"]
    expected_rows = [
        ("http://36.jpg", "monahan93"),
        ("http://25.jpg", "monahan93"),
        ("http://two.jpg", "monahan93"),
        ("http://754.jpg", "pferrer"),
        ("http://35.jpg", "si93onis"),
        ("http://256.jpg", "99stroman"),
        ("http://one.jpg", "99stroman"),
    ]

    columns, rows = peewee_query(
        db=peewee_db,
        sql=pathlib.Path(__file__).parent.joinpath("028e_select.sql").read_text(),
    )

    assert columns == expected_columns
    assert rows == expected_rows


@pytest.mark.usefixtures("_create_users_table", "_create_photos_table")
def test_insert_error(peewee_db):  # noqa: ANN001, ANN201, D103

    key_that_does_not_exist = 9999

    with peewee_db.atomic():  # noqa: SIM117
        with pytest.raises(peewee.IntegrityError) as excinfo:
            peewee_db.execute_sql(
                f"""
                INSERT INTO photos
                    (url, user_id)
                VALUES
                    ('http://jpg', {key_that_does_not_exist});
                """
            )

    assert (
        f'Key (user_id)=({key_that_does_not_exist}) is not present in table "users"'
        in str(excinfo.value)
    )


@pytest.mark.usefixtures("_create_users_table", "_create_photos_table")
def test_insert_with_user_null(peewee_db, peewee_query):  # noqa: ANN001, ANN201, D103
    expected_columns = ["id", "url", "user_id"]
    expected_rows = [
        (1, "http://one.jpg", 4),
        (2, "http://two.jpg", 1),
        (3, "http://25.jpg", 1),
        (4, "http://36.jpg", 1),
        (5, "http://754.jpg", 2),
        (6, "http://35.jpg", 3),
        (7, "http://256.jpg", 4),
        (8, "http://jpg", None),
    ]

    with peewee_db.atomic():
        peewee_db.execute_sql(
            """
            INSERT INTO photos
                (url, user_id)
            VALUES
                ('http://jpg', NULL);
            """
        )

    columns, rows = peewee_query(
        db=peewee_db,
        sql="SELECT * from photos",
    )

    assert columns == expected_columns
    assert rows == expected_rows


@pytest.mark.usefixtures("_create_users_table", "_create_photos_table")
def test_drop_photos(peewee_db, peewee_query):  # noqa: ANN001, ANN201, D103
    expected_columns = ["id", "username"]
    expected_rows = [
        (1, "monahan93"),
        (2, "pferrer"),
        (3, "si93onis"),
        (4, "99stroman"),
    ]

    with peewee_db.atomic():
        peewee_db.execute_sql(
            """
            DROP TABLE photos
            """
        )

    columns, rows = peewee_query(
        db=peewee_db,
        sql="SELECT * from users",
    )

    assert columns == expected_columns
    assert rows == expected_rows


@pytest.mark.usefixtures("_create_users_table", "_create_photos_table")
def test_drop_users_cannot_be_done(peewee_db):  # noqa: ANN001, ANN201, D103

    expected_string = "cannot drop table users because other objects depend on it"

    with peewee_db.atomic():  # noqa: SIM117
        with pytest.raises(peewee.InternalError) as excinfo:
            peewee_db.execute_sql(
                """
                DROP TABLE users
                """
            )

    assert expected_string in str(excinfo.value)


@pytest.mark.usefixtures("_create_users_table", "_create_photos_table")
def test_drop_user_and_cascade(peewee_db, peewee_query):  # noqa: ANN001, ANN201, D103
    expected_users_columns = ["id", "username"]
    expected_users_rows = [(2, "pferrer"), (3, "si93onis"), (4, "99stroman")]
    expected_photos_columns = ["id", "url", "user_id"]
    expected_photos_rows = [
        (1, "http://one.jpg", 4),
        (5, "http://754.jpg", 2),
        (6, "http://35.jpg", 3),
        (7, "http://256.jpg", 4),
    ]

    with peewee_db.atomic():
        peewee_db.execute_sql(
            """
            DELETE FROM users
            WHERE id = 1;
            """
        )

    columns_users, rows_users = peewee_query(
        db=peewee_db,
        sql="SELECT * from users",
    )

    columns_photos, rows_photos = peewee_query(
        db=peewee_db,
        sql="SELECT * from photos",
    )

    assert columns_users == expected_users_columns
    assert rows_users == expected_users_rows

    assert columns_photos == expected_photos_columns
    assert rows_photos == expected_photos_rows


@pytest.mark.usefixtures("_create_users_table")
def test_drop_user_without_cascade_but_with_null(  # noqa: ANN201, D103
    peewee_db, peewee_query  # noqa: ANN001
):  # noqa: ANN001, ANN201, D103, RUF100

    expected_photos_columns = ["id", "url", "user_id"]
    expected_photos_rows = [
        (2, "http:/754.jpg", 2),
        (3, "http:/35.jpg", 3),
        (1, "http:/one.jpg", None),
        (4, "http:/256.jpg", None),
    ]

    with peewee_db.atomic():
        peewee_db.execute_sql(
            """
            CREATE TABLE photos (
                id SERIAL PRIMARY KEY,
                url VARCHAR(200),
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
            );

            INSERT INTO photos (url, user_id)
            VALUES
            ('http:/one.jpg', 4),
            ('http:/754.jpg', 2),
            ('http:/35.jpg', 3),
            ('http:/256.jpg', 4);

            DELETE FROM users
            WHERE id = 4;
            """
        )

    columns_photos, rows_photos = peewee_query(
        db=peewee_db,
        sql="SELECT * from photos",
    )

    assert columns_photos == expected_photos_columns
    assert rows_photos == expected_photos_rows
