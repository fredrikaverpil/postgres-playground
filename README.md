# postgres-playground

[![test](https://github.com/fredrikaverpil/postgres-playground/actions/workflows/test.yml/badge.svg)](https://github.com/fredrikaverpil/postgres-playground/actions/workflows/test.yml)

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
before the test completes and the db is reset. See either of the fixtures in [tests/fixtures/orm/](tests/fixtures/orm/).


Then connect to `localhost` on port `5400`.

### SQL formatting

It's nice to have some sort of formatter/linter. For now,
I'm using [SQLTools](https://github.com/mtxr/vscode-sqltools)
in vscode when saving `.sql` files and occasionally
run [SQLFluff](https://github.com/sqlfluff/sqlfluff).

```bash
pipx install sqlfluff
sqlfluff lint --dialect postgres tests/**/*.sql
sqlfluff fix --dialect postgres tests/**/*.sql
```
