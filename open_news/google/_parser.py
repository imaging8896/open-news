import base64
import json

from datetime import datetime

from html.parser import HTMLParser

from .article import GoogleNewsArticle


class GoogleNewsHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)

        self._entering_title_a = False

        self._stack: list[GoogleNewsArticle] = []

        self.all_news: list[GoogleNewsArticle] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if jslog_str := _get_attribute(attrs, "jslog"):
                if not self._stack:
                    self._stack.append(GoogleNewsArticle(
                        url=None,
                        title=None,
                    ))
                if len(self._stack) != 1:
                    raise RuntimeError(f"There should be article in stack but got {self._stack}")
                
                article = self._stack[0]
                if article.url is not None:
                    raise RuntimeError(f"URL already exists in {article}")

                second_log = jslog_str.split("; ")[1]
                encoded_value = second_log.split(":")[1]
                # In fact, even the linked RFC contains an alternative table for URL and filename safe encoding, 
                # which replaces character '+' and '/' with - and _ respectively)
                decoded_json_str = base64.b64decode(encoded_value.replace("_", "/").replace("-", "+"), validate=True).decode()
                json_data = json.loads(decoded_json_str)
                if isinstance(json_data, list) and json_data:
                    if isinstance(json_data[-1], str):
                        article.url = json_data[-1].strip()

            elif _get_attribute(attrs, "data-n-tid") == "29": 
                self._entering_title_a = True               

        elif tag == "time":
            if datetime_str := _get_attribute(attrs, "datetime"):
                if len(self._stack) != 1:
                    raise RuntimeError(f"There should be article in stack but got {self._stack}")
                article = self._stack.pop()
                if article.url is None:
                    raise RuntimeError(f"URL is None in {article}")
                if article.title is None:
                    raise RuntimeError(f"Title is None in {article}")
                article.publish_time = _workaround_py10_datetime_fromisoformat(datetime_str)
                self.all_news.append(article)
            else:
                raise RuntimeError(f"Time tag but without 'datetime' attribute in {attrs} for stack {self._stack}")

    def handle_endtag(self, tag):
        if tag == "a":
            self._entering_title_a = False

    def handle_data(self, data):
        if self._entering_title_a:
            if stripped_data := data.strip():
                if len(self._stack) == 0:
                    self._stack.append(GoogleNewsArticle(
                        url=None,
                        title=stripped_data,
                    ))
                elif len(self._stack) == 1:
                    article = self._stack[0]
                    if article.title is not None:
                        raise RuntimeError(f"Title already exists in {article} got {stripped_data}")
                    article.title = stripped_data
                else:
                    raise RuntimeError(f"There should be 1 or 0 article in stack but got {self._stack}")



def _get_attribute(attributes: list[tuple[str, str | None]], attribute_name: str) -> str | None:
    if isinstance(attributes, list):
        for name, value in attributes:
            if name == attribute_name:
                return value


def _workaround_py10_datetime_fromisoformat(datetime_str: str):
    import sys
    from datetime import timezone


    if sys.version_info < (3, 11) and datetime_str.strip().endswith("Z"):
        return datetime.fromisoformat(datetime_str.strip()[:-1]).replace(tzinfo=timezone.utc)
    else:
        return datetime.fromisoformat(datetime_str.strip())
