import requests

from ._parser import GoogleNewsHTMLParser
from .constant import Category, Location


def get_news(category: Category, category_id: str, location: Location, section_id: str = None):
    url = _get_google_url(category, category_id, location, section_id=section_id)
    with requests.get(url, timeout=10) as response:
        response.raise_for_status()
        response_text = response.text

        parser = GoogleNewsHTMLParser()
        parser.feed(response_text)
        return parser.all_news


def _get_google_url(category: Category, category_id: str, location: Location, section_id: str = None) -> str:
    if section_id is None:
        return f"https://news.google.com/{category.value}/{category_id}?{location.value}"
    return f"https://news.google.com/{category.value}/{category_id}/sections/{section_id}?{location.value}"
