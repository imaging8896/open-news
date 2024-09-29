import pytest

from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from open_news.google import _parser
from open_news.google.article import GoogleNewsArticle


def test_init():
    with patch.object(_parser.HTMLParser, "__init__", autospec=True) as mock_html_parser___init__:
        mock_arg_convert_charrefs = MagicMock()

        parser = _parser.GoogleNewsHTMLParser(convert_charrefs=mock_arg_convert_charrefs)

        mock_html_parser___init__.assert_called_once_with(parser, convert_charrefs=mock_arg_convert_charrefs)


def test_handle_starttag_for_article_tag():
    parser = _parser.GoogleNewsHTMLParser()
    
    parser.handle_starttag("article", None)

    assert parser._entering_article
    assert not parser._entering_a
    assert parser._cur_article_url is None
    assert parser._cur_article_title is None
    assert parser.all_news == []


@pytest.mark.parametrize("test_attributes,expect_encoded_value", [
    pytest.param([("jslog", "a; b:c; d:e")], "c", id="general"),
    pytest.param([("jslog", "a; b:c-__-_-; d:e")], "c+//+/+", id="Contain base64 safe encoding chars"),
])
@pytest.mark.parametrize("mock_json_decoded_value,expect_url", [
    (["http://a.b.c   "], "http://a.b.c"),
    ([None, None, "   http://a.b.c"], "http://a.b.c"),
    ([None, "   http://a.b.c   "], "http://a.b.c"),
])
def test_handle_starttag_for_a_tag_with_jslog_str_when_entering_article_tag(test_attributes, expect_encoded_value, mock_json_decoded_value, expect_url):
    with (
        patch.object(_parser.base64, "b64decode", autospec=True) as mock_b64decode,
        patch.object(_parser.json, "loads", autospec=True, return_value=mock_json_decoded_value) as mock_json_loads,
    ):
        parser = _parser.GoogleNewsHTMLParser()
        parser._entering_article = True
        
        parser.handle_starttag("a", test_attributes)

        assert parser._entering_a
        assert parser._cur_article_url == expect_url
        assert parser._cur_article_title is None
        assert parser.all_news == []

        mock_b64decode.assert_called_once_with(expect_encoded_value, validate=True)
        mock_json_loads.assert_called_once_with(mock_b64decode.return_value.decode.return_value)


@pytest.mark.parametrize("mock_json_decoded_value", [
    None,
    1,
    1.2,
    "",
    "ddd",
    [],
    [1],
    [None, None, 1.2],
    [None, None, None],
    {},
    {"123": 123, 123: "123"},
])
def test_handle_starttag_for_a_tag_with_jslog_str_but_no_url_in_decoded_string_when_entering_article_tag(mock_json_decoded_value):
    with (
        patch.object(_parser.base64, "b64decode", autospec=True),
        patch.object(_parser.json, "loads", autospec=True, return_value=mock_json_decoded_value),
    ):
        parser = _parser.GoogleNewsHTMLParser()
        parser._entering_article = True
        
        parser.handle_starttag("a", [("jslog", "a; b:c; d:e")])

        assert parser._entering_a
        assert parser._cur_article_url is None
        assert parser._cur_article_title is None
        assert parser.all_news == []

@pytest.mark.parametrize("test_attributes", [
    None,
    [],
    [("a", "v")],
    [("a", "v"), ("d", "e")],
])
def test_handle_starttag_for_a_tag_without_jslog_str_when_entering_article_tag(test_attributes):
    parser = _parser.GoogleNewsHTMLParser()
    parser._entering_article = True
    
    parser.handle_starttag("a", test_attributes)

    assert parser._entering_a
    assert parser._cur_article_url is None
    assert parser._cur_article_title is None
    assert parser.all_news == []


def test_handle_starttag_for_time_tag_when_entering_article_tag():
    parser = _parser.GoogleNewsHTMLParser()
    parser._entering_article = True
    parser._cur_article_title = "title"
    parser._cur_article_url = "url"
    
    parser.handle_starttag("time", [("datetime", "2024-09-17T03:30:00Z")])

    assert not parser._entering_a
    assert parser._cur_article_url is None
    assert parser._cur_article_title is None
    assert parser.all_news == [
        GoogleNewsArticle(
            title="title",
            url="url", 
            publish_time=datetime(year=2024, month=9, day=17, hour=3, minute=30, second=0, tzinfo=timezone.utc),
        )
    ]


def test_handle_starttag_for_time_tag_raise_runtime_error_when_no_title_when_entering_article_tag():
    parser = _parser.GoogleNewsHTMLParser()
    parser._entering_article = True
    parser._cur_article_url = None

    with pytest.raises(RuntimeError):    
        parser.handle_starttag("time", [("datetime", "2024-09-17T03:30:00Z")])


def test_handle_starttag_for_time_tag_raise_runtime_error_when_no_url_when_entering_article_tag():
    parser = _parser.GoogleNewsHTMLParser()
    parser._entering_article = True
    parser._cur_article_title = "title"
    parser._cur_article_url = None

    with pytest.raises(RuntimeError):    
        parser.handle_starttag("time", [("datetime", "2024-09-17T03:30:00Z")])


@pytest.mark.parametrize("test_attributes", [
    None,
    [],
    [("a", "v")],
    [("a", "v"), ("d", "e")],
])
def test_handle_starttag_for_time_tag_raise_runtime_error_when_no_datetime_attribute_when_entering_article_tag(test_attributes):
    parser = _parser.GoogleNewsHTMLParser()
    parser._entering_article = True
    parser._cur_article_title = "title"
    parser._cur_article_url = "url"

    with pytest.raises(RuntimeError):    
        parser.handle_starttag("time", test_attributes)


@pytest.mark.parametrize("origin_entering_article", [True, False])
def test_handle_endtag_for_article_tag(origin_entering_article):
    parser = _parser.GoogleNewsHTMLParser()
    parser._entering_article = origin_entering_article

    parser.handle_endtag("article")

    assert not parser._entering_article


@pytest.mark.parametrize("origin_entering_a", [True, False])
def test_handle_endtag_for_a_tag(origin_entering_a):
    parser = _parser.GoogleNewsHTMLParser()
    parser._entering_a = origin_entering_a

    parser.handle_endtag("a")

    assert not parser._entering_a


@pytest.mark.parametrize("mock_data,expect_article_title", [
    pytest.param("asd", "asd", id="General"),
    pytest.param("   asd", "asd", id="Leading spaces"),
    pytest.param("asd     ", "asd", id="Following spaces"),
    pytest.param("   asd     ", "asd", id="Leading and following spaces"),
    pytest.param("\n   asd\n ", "asd", id="Leading and following spaces or newlines"),
])
def test_handle_data_entering_a_in_an_article(mock_data, expect_article_title):
    parser = _parser.GoogleNewsHTMLParser()
    parser._entering_article = True
    parser._entering_a = True

    parser.handle_data(mock_data)

    assert parser._cur_article_title == expect_article_title



@pytest.mark.parametrize("entering_article,entering_a,mock_data", [
    (False, True, "asd"),
    (False, False, "asd"),
    (False, True, ""),
    (False, True, "   \n"),
    (False, False, "\n "),
    (True, False, "asd"),
    (True, True, "   "),
    (True, False, "\n"),
    (True, True, " "),
])
def test_handle_data_no_article_title_got(entering_article, entering_a, mock_data):
    parser = _parser.GoogleNewsHTMLParser()
    parser._entering_article = entering_article
    parser._entering_a = entering_a

    parser.handle_data(mock_data)

    assert parser._cur_article_title is None
