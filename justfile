check: lint type-check test

lint:
    uv run ruff check .
    uv run ruff format --check .

type-check:
    uv run mypy .

test:
    uv run pytest
