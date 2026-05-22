from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel, HttpUrl


class BlogSource(BaseModel):
    name: str
    url: HttpUrl
    feed_url: HttpUrl


def load_sources(path: str = "sources.yaml") -> List[BlogSource]:
    with open(Path(path)) as file:
        data = yaml.safe_load(file)
    return [BlogSource(**entry) for entry in data]
