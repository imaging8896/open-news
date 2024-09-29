import time

from datetime import datetime

from open_news.google.feed import get_feed
from open_news.google.feed.article import GoogleFeedArticle


def test_get_feed(google_news_request):
    category, category_id, location, section_id = google_news_request

    try:
        results = get_feed(category, category_id, location, section_id=section_id)
        assert len(results) == 1
        for channel in results:
            assert isinstance(channel.update_time, datetime)
            assert isinstance(channel.items, list)

            for item in channel.items:
                assert isinstance(item.publish_time, datetime)
                
                assert isinstance(item.id, str)
                assert item.id != ""

                assert isinstance(item.main_article, GoogleFeedArticle)

                assert isinstance(item.title, str)
                assert item.title != ""

                assert isinstance(item.url, str)
                assert item.url != ""

                for article in item.articles:
                    assert isinstance(article.id, str)
                    assert article.id != ""

                    assert isinstance(article.title, str)
                    assert article.title != ""

                    assert isinstance(article.url, str)
                    assert article.url.startswith("http")

                    if article.story_url is not None:
                        assert isinstance(article.story_url, str)
                        assert article.url != ""

                    assert article.publish_time is None
    finally:
        time.sleep(3)
