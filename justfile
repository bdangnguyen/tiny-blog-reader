check: lint type-check test

lint:
    uv run ruff check --fix . 
    uv run ruff format .

type-check:
    uv run mypy .

test:
    uv run pytest
