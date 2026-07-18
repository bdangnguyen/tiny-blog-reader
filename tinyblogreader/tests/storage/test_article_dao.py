import pytest

from tinyblogreader.storage.article_dao import Article, ArticleDAO
from tinyblogreader.storage.db import get_connection


@pytest.fixture
def dao():
    conn = get_connection(":memory:")
    yield ArticleDAO(conn)
    conn.close()


def _make_article(**kwargs) -> Article:
    defaults = {
        "id": "abc123",
        "source": "Netflix Tech Blog",
        "title": "How We Build Things",
        "url": "https://example.com/article",
        "content": "Some content here.",
    }
    return Article(**{**defaults, **kwargs})


def test_insert_and_exists(dao):
    article = _make_article()
    dao.insert(article)
    assert dao.exists(article.id)


def test_exists_returns_false_for_missing(dao):
    assert not dao.exists("nonexistent-id")


def test_insert_duplicate_raises(dao):
    article = _make_article()
    dao.insert(article)
    with pytest.raises(Exception):
        dao.insert(article)


def test_insert_duplicate_url_raises(dao):
    dao.insert(_make_article(id="id-1"))
    with pytest.raises(Exception):
        dao.insert(_make_article(id="id-2"))


def test_exists_does_not_match_other_ids(dao):
    dao.insert(_make_article(id="id-a"))
    assert not dao.exists("id-b")


def test_insert_persists_all_fields(dao):
    article = _make_article()
    dao.insert(article)
    cursor = dao.conn.execute("SELECT * FROM articles WHERE id = ?", (article.id,))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == article.id
    assert row[1] == article.source
    assert row[2] == article.title
    assert row[3] == article.url
    assert row[4] == article.content
