from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class GoogleNewsArticle:
    title: str
    url: str
    story_url: str | None = None
    publish_time: datetime | None = None

    @property
    def id(self) -> str:
        return self.url
