import xml.etree.ElementTree as ET

from .channel import GoogleFeedChannel
from ..constant import Category, Location
from ..request import request_get


def get_feed(category: Category, category_id: str, location: Location, section_id: str | None = None) -> list[GoogleFeedChannel]:
    url = _get_google_feed_url(category, category_id, location, section_id)

    response_text = request_get(url, timeout=10)

    return [
        GoogleFeedChannel.create(child)
        for child in ET.fromstring(response_text)
            if child.tag == "channel"
        ]

def _get_google_feed_url(category: Category, category_id: str, location: Location, section_id: str | None = None) -> str:
    if section_id is None:
        return f"https://news.google.com/rss/{category.value}/{category_id}?{location.value}"
    return f"https://news.google.com/rss/{category.value}/{category_id}/sections/{section_id}?{location.value}"
