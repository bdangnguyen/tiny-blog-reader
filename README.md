# tiny-blog-reader

A content-based recommendation system for engineering blog articles. Scrapes RSS feeds, stores articles locally, and recommends new reads based on your reading history.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just)

## Setup

```bash
uv sync
```

## Development

```bash
just check       # run lint, type-check, and tests
just lint        # ruff check + format
just type-check  # mypy
just test        # pytest
```
