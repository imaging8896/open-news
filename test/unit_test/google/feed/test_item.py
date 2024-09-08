import pytest

from unittest.mock import MagicMock, patch
from datetime import datetime

from open_news.google.feed import item


def test_main_article_property():
    article1 = item.GoogleFeedArticle(title="title1", url="url1", story_url="story_url1")
    article2 = item.GoogleFeedArticle(title="title2", url="url2", story_url="story_url2")
    article3 = item.GoogleFeedArticle(title="title3", url="url3", story_url="story_url3")
    assert item.GoogleFeedItem(
        articles=[article1, article2, article3], 
        publish_time=datetime.now(),
    ).main_article == article1


def test_id_property():
    article1 = item.GoogleFeedArticle(title="title1", url="url1", story_url="story_url1")
    article2 = item.GoogleFeedArticle(title="title2", url="url2", story_url="story_url2")
    article3 = item.GoogleFeedArticle(title="title3", url="url3", story_url="story_url3")
    assert item.GoogleFeedItem(
        articles=[article1, article2, article3], 
        publish_time=datetime.now(),
    ).id == article1.url


def test_title_property():
    article1 = item.GoogleFeedArticle(title="title1", url="url1", story_url="story_url1")
    article2 = item.GoogleFeedArticle(title="title2", url="url2", story_url="story_url2")
    article3 = item.GoogleFeedArticle(title="title3", url="url3", story_url="story_url3")
    assert item.GoogleFeedItem(
        articles=[article1, article2, article3], 
        publish_time=datetime.now(),
    ).title == article1.title


def test_url_property():
    article1 = item.GoogleFeedArticle(title="title1", url="url1", story_url="story_url1")
    article2 = item.GoogleFeedArticle(title="title2", url="url2", story_url="story_url2")
    article3 = item.GoogleFeedArticle(title="title3", url="url3", story_url="story_url3")
    assert item.GoogleFeedItem(
        articles=[article1, article2, article3], 
        publish_time=datetime.now(),
    ).url == article1.url


@pytest.fixture
def mock_get_element_first_child():
    with patch.object(item, "get_element_first_child", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_article_class_create_from_description_with_stories():
    with patch.object(item.GoogleFeedArticle, "create_from_description_with_stories", autospec=True) as mock:
        mock.return_value = [MagicMock(), MagicMock(), MagicMock()]
        yield mock


@pytest.fixture
def mock_article_class_create_from_description_with_story():
    with patch.object(item.GoogleFeedArticle, "create_from_description_with_story", autospec=True) as mock:
        mock.return_value = [MagicMock()]
        yield mock


MOCK_DATETIME_STR = "Fri, 06 Sep 2024 00:12:25 GMT"
MOCK_DATETIME = datetime(year=2024, month=9, day=6, hour=0, minute=12, second=25)


def _mock_element(text: str):
    from xml.etree.ElementTree import Element

    mock = MagicMock(spec=Element)
    mock.text = text
    return mock


@pytest.mark.parametrize("description_text,expect_description_text", [
    pytest.param(
        "<ol>...",
        "<ol>...",
        id="General",
    ),
    pytest.param(
        """  
          <ol>... 
            """,
        "<ol>...",
        id="With prefix and suffix spaces and newline",
    ),
    pytest.param(
        "<ol&nbsp;>.&nbsp;..",
        "<ol>...",
        id="With &nbsp; xml escape char",
    ),
])
def test_create_from_ol_tag_article(
    description_text, 
    expect_description_text,
    mock_get_element_first_child: MagicMock,
    mock_article_class_create_from_description_with_stories: MagicMock,
    mock_article_class_create_from_description_with_story: MagicMock,
):
    mock_root_element = MagicMock()

    def _mock_get_element_first_child_side_effect(the_element, tag: str):
        assert the_element is mock_root_element
        
        if tag == "pubDate":
            return _mock_element(MOCK_DATETIME_STR)
        elif tag == "title":
            return _mock_element("title 1    ")
        elif tag == "link":
            return _mock_element("""
                                     https://123.123.123 
                                    """)
        elif tag == "description":
            return _mock_element(description_text)

    mock_get_element_first_child.side_effect = _mock_get_element_first_child_side_effect

    the_item = item.GoogleFeedItem.create(mock_root_element)

    assert the_item.publish_time == MOCK_DATETIME
    
    first_article = the_item.articles[0]
    assert first_article.title == "title 1"
    assert first_article.url == "https://123.123.123"
    assert first_article.story_url is None

    assert the_item.articles[1:] == mock_article_class_create_from_description_with_stories.return_value

    mock_article_class_create_from_description_with_stories.assert_called_once_with(expect_description_text)
    mock_article_class_create_from_description_with_story.assert_not_called()


@pytest.mark.parametrize("description_text,expect_description_text", [
    pytest.param(
        "<a ...",
        "<a ...",
        id="General",
    ),
    pytest.param(
        """  
          <a ... 
            """,
        "<a ...",
        id="With prefix and suffix spaces and newline",
    ),
    pytest.param(
        "<a &nbsp;.&nbsp;..",
        "<a ...",
        id="With &nbsp; xml escape char",
    ),
])
def test_create_from_a_tag_article(
    description_text, 
    expect_description_text,
    mock_get_element_first_child: MagicMock,
    mock_article_class_create_from_description_with_stories: MagicMock,
    mock_article_class_create_from_description_with_story: MagicMock,
):
    mock_root_element = MagicMock()

    def _mock_get_element_first_child_side_effect(the_element, tag: str):
        assert the_element is mock_root_element

        if tag == "pubDate":
            return _mock_element(MOCK_DATETIME_STR)
        elif tag == "title":
            return _mock_element("title 1    ")
        elif tag == "link":
            return _mock_element("""
                                     https://123.123.123 
                                    """)
        elif tag == "description":
            return _mock_element(description_text)

    mock_get_element_first_child.side_effect = _mock_get_element_first_child_side_effect

    the_item = item.GoogleFeedItem.create(mock_root_element)

    assert the_item.publish_time == MOCK_DATETIME
    
    first_article = the_item.articles[0]
    assert first_article.title == "title 1"
    assert first_article.url == "https://123.123.123"
    assert first_article.story_url is None

    assert the_item.articles[1:] == mock_article_class_create_from_description_with_story.return_value

    mock_article_class_create_from_description_with_stories.assert_not_called()
    mock_article_class_create_from_description_with_story.assert_called_once_with(expect_description_text)


@pytest.mark.parametrize("description_text", ["", "asd", "<li>", "<b>", "<al"])
def test_create_raise_WrongNewsXML_FormatError_if_description_text_not_start_with_ol_or_a_tag(
    description_text, 
    mock_get_element_first_child: MagicMock,
):
    mock_element = _mock_element("don't care")

    def _mock_get_element_first_child_side_effect(_, tag: str):
        if tag == "pubDate":
            return _mock_element(MOCK_DATETIME_STR)
        elif tag == "title":
            return mock_element
        elif tag == "link":
            return mock_element
        elif tag == "description":
            return _mock_element(description_text)

    mock_get_element_first_child.side_effect = _mock_get_element_first_child_side_effect

    with patch.object(item.ET, "tostring", autospec=True):
        with pytest.raises(item.WrongNewsXML_FormatError):
            item.GoogleFeedItem.create(MagicMock())
