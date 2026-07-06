import sqlite3

import pytest

from tinyblogreader.storage.db import get_connection


@pytest.fixture
def conn():
    return get_connection(":memory:")


def test_get_connection_returns_connection(conn):
    assert isinstance(conn, sqlite3.Connection)


def test_get_connection_applies_schema(conn):
    conn.execute("SELECT * FROM articles")


def test_get_connection_sets_wal(tmp_path):
    db_path = tmp_path / "test.db"

    conn = get_connection(db_path)
    row = conn.execute("PRAGMA journal_mode").fetchone()

    assert row[0] == "wal"


def test_get_connection_is_idempotent(tmp_path):
    db_path = tmp_path / "test.db"

    get_connection(db_path)
    get_connection(db_path)


def test_get_connection_custom_path(tmp_path):
    db_path = tmp_path / "test.db"

    get_connection(db_path)

    assert db_path.exists()


def test_get_connection_creates_directory(tmp_path, monkeypatch):
    missing_dir = tmp_path / "nested" / "test.db"
    monkeypatch.setattr(
        "tinyblogreader.storage.db.user_data_dir", lambda _: missing_dir
    )

    get_connection()

    assert missing_dir.exists()
