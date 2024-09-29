import base64
import json

from datetime import datetime

from html.parser import HTMLParser

from .article import GoogleNewsArticle


class GoogleNewsHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)

        self._entering_article = False
        self._entering_a = False

        self._cur_article_url = None
        self._cur_article_title = None

        self.all_news: list[GoogleNewsArticle] = []

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self._entering_article = True

        elif self._entering_article:
            if tag == "a":
                self._entering_a = True

                if jslog_str := _get_attribute(attrs, "jslog"):
                    second_log = jslog_str.split("; ")[1]
                    encoded_value = second_log.split(":")[1]
                    # In fact, even the linked RFC contains an alternative table for URL and filename safe encoding, 
                    # which replaces character '+' and '/' with - and _ respectively)
                    decoded_json_str = base64.b64decode(encoded_value.replace("_", "/").replace("-", "+"), validate=True).decode()
                    json_data = json.loads(decoded_json_str)
                    if isinstance(json_data, list) and json_data:
                        if isinstance(json_data[-1], str):
                            self._cur_article_url = json_data[-1].strip()
                        # elif isinstance(json_data[-1], list):
                        #     if results := [x for x in json_data[-1] if x is not None]:
                        #         # Story id
                        #         self._cur_article_story_id = results[0].strip()

            elif tag == "time":
                if self._cur_article_title is None:
                    raise RuntimeError(f"Article without title but publish time tag with attributes {attrs}")
                if self._cur_article_url is None:
                    raise RuntimeError(f"Article with title '{self._cur_article_title}' has no news link")

                if datetime_str := _get_attribute(attrs, "datetime"):
                    self.all_news.append(
                        GoogleNewsArticle(
                            title=self._cur_article_title,
                            url=self._cur_article_url, 
                            publish_time=datetime.fromisoformat(datetime_str.strip()),
                        )
                    )
                    self._cur_article_url, self._cur_article_title = None, None
                else:
                    raise RuntimeError(f"Article with title '{self._cur_article_title}' has time tag but without 'datetime' attribute in {attrs}")

    def handle_endtag(self, tag):
        if tag == "article":
            self._entering_article = False
        elif tag == "a":
            self._entering_a = False

    def handle_data(self, data):
        if self._entering_article:
            if self._entering_a:
                if stripped_data := data.strip():
                    self._cur_article_title = stripped_data


def _get_attribute(attributes: list[tuple[str, str]], attribute_name: str) -> str | None:
    if isinstance(attributes, list):
        for name, value in attributes:
            if name == attribute_name:
                return value
