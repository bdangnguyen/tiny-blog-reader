import sqlite3
from pathlib import Path

from platformdirs import user_data_dir

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection(db_path: Path | str | None = None) -> sqlite3.Connection:
    if db_path is None:
        data_dir = Path(user_data_dir("tiny_blog_reader"))
        data_dir.mkdir(parents=True, exist_ok=True)
        db_path = data_dir / "tiny_blog_reader.db"

    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_PATH.read_text())
    conn.execute("PRAGMA journal_mode=WAL")
    return conn
