import time, pytest

from datetime import datetime

from open_news.google.feed import get_feed, Category, Location
from open_news.google.feed.article import GoogleFeedArticle



@pytest.mark.parametrize("category,category_id", [
    (
        Category.TOPICS, 
        "CAAqJQgKIh9DQkFTRVFvSUwyMHZNREpmTjNRU0JYcG9MVlJYS0FBUAE",
    )
])
@pytest.mark.parametrize("location", [Location.Taiwan])
@pytest.mark.parametrize("section_id", [
    None,
    "CAQiW0NCQVNQZ29JTDIwdk1ESmZOM1FTQlhwb0xWUlhJZzhJQkJvTENna3ZiUzh3T1hrMGNHMHFHZ29ZQ2hSTlFWSkxSVlJUWDFORlExUkpUMDVmVGtGTlJTQUJLQUEqKQgAKiUICiIfQ0JBU0VRb0lMMjB2TURKZk4zUVNCWHBvTFZSWEtBQVABUAE",
])
def test_get_feed(category, category_id, location, section_id):
    try:
        results = get_feed(category, category_id, location, section_id=section_id)
        assert len(results) == 1
        for channel in results:
            assert isinstance(channel.update_time, datetime)
            assert isinstance(channel.items, list)
            assert len(channel.items) > 0

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
                    assert article.url != ""

                    if article.story_url is not None:
                        assert isinstance(article.story_url, str)
                        assert article.url != ""
    finally:
        time.sleep(3)
