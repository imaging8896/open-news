from open_news.google import article


def test_init():
    article.GoogleNewsArticle(title="the title", url="the url", story_url="the story url")


def test_init_without_story_url():
    article.GoogleNewsArticle(title="the title", url="the url")


def test_id_property():
    assert article.GoogleNewsArticle(title="the title", url="the url", story_url="the story url").id == "the url"
