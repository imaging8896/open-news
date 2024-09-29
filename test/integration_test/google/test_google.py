import time, pytest

from datetime import datetime

from open_news.google import get_news


def test_get_news(google_news_request):
    category, category_id, location, section_id = google_news_request
    try:
        results = get_news(category, category_id, location, section_id=section_id)
        for article in results:
            assert isinstance(article.id, str)
            assert article.id != ""

            assert isinstance(article.title, str)
            assert article.title != ""

            assert isinstance(article.url, str)
            assert article.url.startswith("http")

            assert article.story_url is None

            assert isinstance(article.publish_time, datetime)
    finally:
        time.sleep(3)
