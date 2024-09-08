import requests
import xml.etree.ElementTree as ET

from .constant import Category, Location
from .channel import GoogleFeedChannel


def get_feed(category: Category, category_id: str, location: Location, section_id: str = None) -> list[GoogleFeedChannel]:
    url = _get_google_feed_url(category, category_id, location, section_id)

    with requests.get(url, timeout=10) as response:
        response.raise_for_status()

        return [
            GoogleFeedChannel.create(child)
            for child in ET.fromstring(response.text)
            if child.tag == "channel"
        ]

def _get_google_feed_url(category: Category, category_id: str, location: Location, section_id: str = None) -> str:
    if section_id is None:
        return f"https://news.google.com/rss/{category.value}/{category_id}?{location.value}"
    return f"https://news.google.com/rss/{category.value}/{category_id}/sections/{section_id}?{location.value}"
