import os

import pytest
from playhouse.db_url import connect

DB = os.environ.get(
    "DB_CONN_POSTGRES", "postgres://postgres:secret@localhost:5400/postgres"
)


@pytest.fixture
def peewee_db():
    # https://docs.peewee-orm.com/en/latest/peewee/database.html

    db = connect(DB)
    # db.connect()

    yield db

    with db.atomic():
        drop_schema = """
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;

            GRANT ALL ON SCHEMA public TO postgres;
            GRANT ALL ON SCHEMA public TO public;
        """
        db.execute_sql(drop_schema)

    db.close()
