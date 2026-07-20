check: lint type-check test

lint:
    uv run ruff check --fix . 
    uv run ruff format .

type-check:
    uv run basedpyright .

test:
    uv run pytest
