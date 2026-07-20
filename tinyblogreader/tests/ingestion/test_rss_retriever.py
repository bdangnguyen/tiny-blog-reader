from types import SimpleNamespace
from typing import Callable

from pytest import MonkeyPatch

from tinyblogreader.ingestion.rss_retriever import RawArticle, fetch_feed


def _fake_parse(entries: list[dict[str, str]]) -> Callable[[str], SimpleNamespace]:
    return lambda feed_url: SimpleNamespace(entries=entries)


def test_fetch_feed_returns_articles(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "tinyblogreader.ingestion.rss_retriever.feedparser.parse",
        _fake_parse(
            [
                {
                    "title": "A blog",
                    "link": "https://example.com/article",
                    "description": "A summary of the article.",
                }
            ]
        ),
    )

    articles = fetch_feed("https://example.com/feed")

    assert articles == [
        RawArticle(
            title="A blog",
            link="https://example.com/article",
            description="A summary of the article.",
        )
    ]


def test_fetch_feed_handles_missing_fields(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "tinyblogreader.ingestion.rss_retriever.feedparser.parse",
        _fake_parse([{}]),
    )

    articles = fetch_feed("https://example.com/feed")

    assert articles == [RawArticle(title="", link="", description="")]


def test_fetch_feed_returns_empty_list_for_no_entries(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "tinyblogreader.ingestion.rss_retriever.feedparser.parse",
        _fake_parse([]),
    )

    assert fetch_feed("https://example.com/feed") == []


def test_fetch_feed_returns_empty_list_on_parse_error(monkeypatch: MonkeyPatch):
    def raise_error(_feed_url: str) -> SimpleNamespace:
        raise ValueError("boom")

    monkeypatch.setattr(
        "tinyblogreader.ingestion.rss_retriever.feedparser.parse", raise_error
    )

    assert fetch_feed("https://example.com/feed") == []
