from dataclasses import dataclass

import feedparser


@dataclass
class RawArticle:
    title: str
    link: str
    description: str


def fetch_feed(feed_url: str):
    try:
        raw_data = feedparser.parse(feed_url)

        return [
            RawArticle(
                title=entry.get("title", ""),
                link=entry.get("link", ""),
                description=entry.get("description", ""),
            )
            for entry in raw_data.entries
        ]
    except Exception:
        return []
