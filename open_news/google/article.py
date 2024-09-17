from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class GoogleNewsArticle:
    title: str
    url: str
    story_url: str = None

    @property
    def id(self) -> str:
        return self.url
