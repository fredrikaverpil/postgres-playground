# postgres-playground

This is a personal testing playground of raw SQL queries and ORM queries for PostgreSQL written in Python,
leveraging the Pytest framework. This allows for quick iteration and debugging when trying new stuff out.

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
docker compose down --volumes --remove-orphans
```

## Debug

### Inspect database

To inspect the database while writing/running tests, set a breakpoint
before the test completes. Example:

```python
def test_peewee_create_tables(peewee_db):
    sql = """
    CREATE TABLE cities (
        name VARCHAR(50),
        country VARCHAR(50),
        population INTEGER,
        area INTEGER
    );
    """

    with peewee_db.atomic():
        peewee_db.execute_sql(sql)

    print("set_breakpoint_here")  # <--- breakpoint on this line and inspect db
```

Then connect to `localhost` on port `5400`.

### Fix SQL linting

```bash
sqlfluff fix --dialect postgres tests/**/*.sql
```
