import xml.etree.ElementTree as ET

from xml.etree.ElementTree import Element
from datetime import datetime
from dataclasses import dataclass

from ._util import get_element_first_child, TIME_FORMAT
from .article import GoogleFeedArticle
from .exception import WrongNewsXML_FormatError


@dataclass(frozen=True, slots=True, kw_only=True)
class GoogleFeedItem:
    articles: list[GoogleFeedArticle]
    publish_time: datetime

    @property
    def main_article(self) -> GoogleFeedArticle:
        return self.articles[0]

    @property
    def id(self) -> str:
        return self.main_article.url
    
    @property
    def title(self) -> str:
        return self.main_article.title
    
    @property
    def url(self) -> str:
        return self.main_article.url

    @classmethod
    def create(clz, item: Element):
        return clz(
            publish_time=datetime.strptime(get_element_first_child(item, "pubDate").text.strip(), TIME_FORMAT),
            articles=[
                GoogleFeedArticle(
                    title=get_element_first_child(item, "title").text.strip(),
                    url=get_element_first_child(item, "link").text.strip(),
                ),
                *clz._get_articles_from_description(get_element_first_child(item, "description"))
            ]
        )

    @staticmethod
    def _get_articles_from_description(description: Element) -> list[GoogleFeedArticle]:
        description_text = description.text.strip().replace("&nbsp;", "")

        if description_text.startswith("<ol>"):
            return GoogleFeedArticle.create_from_description_with_stories(description_text)
        elif description_text.startswith("<a "):
            return GoogleFeedArticle.create_from_description_with_story(description_text)
        else:
            raise WrongNewsXML_FormatError(f"Prefix should one of '<ol>' or '<a' for\n{ET.tostring(description, encoding='unicode')}")
