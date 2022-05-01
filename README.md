# learning-postgresql

This is a personal "notebook" of raw SQL queries and ORM queries for PostgreSQL,
written in Python with Pytest.

# Quickstart

## Run

Run everything within containers:

```bash
docker compose build
docker compose up postgres --detach
docker compose run --rm pytest
docker compose down --volumes --remove-orphans
```

Run db in container and pytest locally:

```bash
poetry install
docker compose up postgres --detach
poetry run pytest
```

## Debug

To inspect the database while writing/running tests, set a breakpoint
before the test completes. Example:

```python
def test_peewee_create_tables(peewee_db):
    sql = """
    CREATE TABLE Persons (
        PersonID int,
        LastName varchar(255),
        FirstName varchar(255),
        Address varchar(255),
        City varchar(255)
    );
    """

    with peewee_db.atomic():
        peewee_db.execute_sql(sql)

    print("set_breakpoint_here")  # <--- breakpoint on this line and inspect db
```

Then connect to `localhost` on port `5400`.
