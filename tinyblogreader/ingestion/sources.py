from pathlib import Path

import yaml
from pydantic import BaseModel, HttpUrl


class BlogSource(BaseModel):
    name: str
    url: HttpUrl
    feed_url: HttpUrl


def load_sources(path: str | Path = "sources.yaml") -> list[BlogSource]:
    with open(Path(path)) as file:
        data = yaml.safe_load(file)
    return [BlogSource.model_validate(entry) for entry in data]
