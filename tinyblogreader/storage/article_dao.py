import sqlite3
from dataclasses import dataclass


@dataclass
class Article:
    id: str
    source: str
    title: str
    url: str
    content: str


class ArticleDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn: sqlite3.Connection = conn

    def insert(self, article: Article) -> None:
        _ = self.conn.execute(
            """
            INSERT INTO articles(id, source, title, url, content) VALUES
                (?, ?, ?, ?, ?)
        """,
            (article.id, article.source, article.title, article.url, article.content),
        )
        self.conn.commit()

    def exists(self, article_id: str) -> bool:
        cursor = self.conn.execute("SELECT 1 FROM articles WHERE id = ?", (article_id,))
        return cursor.fetchone() is not None
