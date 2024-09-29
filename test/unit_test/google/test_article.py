from datetime import datetime

from open_news.google import article


def test_init():
    article.GoogleNewsArticle(title="the title", url="the url", story_url="the story url", publish_time=datetime.now())


def test_init_without_story_url():
    article.GoogleNewsArticle(title="the title", url="the url", publish_time=datetime.now())


def test_init_without_publish_time():
    article.GoogleNewsArticle(title="the title", url="the url", story_url="xxx")


def test_id_property():
    assert article.GoogleNewsArticle(title="the title", url="the url", story_url="the story url").id == "the url"
