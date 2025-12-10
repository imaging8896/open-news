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


class TestTitleATagHandling:

    def test_handle_starttag(self):
        parser = _parser.GoogleNewsHTMLParser()
        
        parser.handle_starttag("a", [("data-n-tid", "29")])

        assert parser._entering_title_a
        assert parser.all_news == []

    def test_handle_endtag(self):
        parser = _parser.GoogleNewsHTMLParser()
        
        parser.handle_endtag("a")

        assert not parser._entering_title_a
        assert parser.all_news == []

    def test_handle_starttag_to_endtag(self):
        parser = _parser.GoogleNewsHTMLParser()
        
        parser.handle_starttag("a", [("data-n-tid", "29")])
        parser.handle_endtag("a")

        assert not parser._entering_title_a
        assert parser.all_news == []

    @pytest.mark.parametrize("mock_data, expect_title", [
        pytest.param("Some Title", "Some Title", id="General"),
        pytest.param("   Some Title   ", "Some Title", id="Leading and trailing spaces"),
        pytest.param("\nSome Title\n", "Some Title", id="Leading and trailing newlines"),
        pytest.param("   \nSome Title\n   ", "Some Title", id="Leading and trailing spaces and newlines"),
    ])
    def test_handle_data_new_data(self, mock_data, expect_title):
        parser = _parser.GoogleNewsHTMLParser()
        parser._entering_title_a = True
        
        parser.handle_data(mock_data)

        assert parser._entering_title_a
        assert len(parser._stack) == 1
        actual_article = parser._stack[0]
        assert actual_article.title == expect_title
        assert actual_article.url is None
        assert actual_article.publish_time is None
        assert parser.all_news == []

    @pytest.mark.parametrize("mock_data, expect_title", [
        pytest.param("Another Title", "Another Title", id="General"),
        pytest.param("   Another Title   ", "Another Title", id="Leading and trailing spaces"),
        pytest.param("\nAnother Title\n", "Another Title", id="Leading and trailing newlines"),
        pytest.param("   \nAnother Title\n   ", "Another Title", id="Leading and trailing spaces and newlines"),
    ])
    def test_handle_data_existing_data(self, mock_data, expect_title):
        parser = _parser.GoogleNewsHTMLParser()
        parser._entering_title_a = True
        parser._stack = [GoogleNewsArticle(url="http://example.com", title=None)]
        
        parser.handle_data(mock_data)

        assert parser._entering_title_a
        assert len(parser._stack) == 1
        actual_article = parser._stack[0]
        assert actual_article.title == expect_title
        assert actual_article.url == "http://example.com"
        assert actual_article.publish_time is None
        assert parser.all_news == []

    def test_handle_data_multiple_data(self):
        parser = _parser.GoogleNewsHTMLParser()
        parser._entering_title_a = True
        parser._stack = [
            GoogleNewsArticle(url="http://example1.com", title=None),
            GoogleNewsArticle(url="http://example2.com", title=None),
        ]
        
        with pytest.raises(RuntimeError):
            parser.handle_data("Some Title")
        assert parser.all_news == []


class TestTimeTagHandling:

    def test_handle_starttag(self):
        parser = _parser.GoogleNewsHTMLParser()
        article = GoogleNewsArticle(
            title="Some Title",
            url="http://example.com",
        )
        parser._stack.append(article)
        
        parser.handle_starttag("time", [("datetime", "2024-09-17T03:30:00Z")])

        assert len(parser.all_news) == 1
        actual_article = parser.all_news[0]
        assert actual_article.title == "Some Title"
        assert actual_article.url == "http://example.com"
        assert actual_article.publish_time == datetime(
            year=2024, month=9, day=17, hour=3, minute=30, second=0, tzinfo=timezone.utc
        )

    def test_handle_starttag_no_datetime_attribute(self):
        parser = _parser.GoogleNewsHTMLParser()
        article = GoogleNewsArticle(
            title="Some Title",
            url="http://example.com",
        )
        parser._stack.append(article)
        
        with pytest.raises(RuntimeError):
            parser.handle_starttag("time", [("data-n-tid", "some_value")])
        assert parser.all_news == []

    def test_handle_starttag_multiple_articles_in_stack(self):
        parser = _parser.GoogleNewsHTMLParser()
        parser._stack = [
            GoogleNewsArticle(
                title="Some Title",
                url="http://example1.com",
            ),
            GoogleNewsArticle(
                title="Some Title",
                url="http://example2.com",
            ),
        ]
        
        with pytest.raises(RuntimeError):
            parser.handle_starttag("time", [("datetime", "2024-09-17T03:30:00Z")])
        assert parser.all_news == []

    def test_handle_starttag_no_title_article(self):
        parser = _parser.GoogleNewsHTMLParser()
        parser._stack = [
            GoogleNewsArticle(
                title=None,
                url="http://example1.com",
            ),
        ]
        
        with pytest.raises(RuntimeError):
            parser.handle_starttag("time", [("datetime", "2024-09-17T03:30:00Z")])
        assert parser.all_news == []

    def test_handle_starttag_no_url_article(self):
        parser = _parser.GoogleNewsHTMLParser()
        parser._stack = [
            GoogleNewsArticle(
                title="Some Title",
                url=None,
            ),
        ]
        
        with pytest.raises(RuntimeError):
            parser.handle_starttag("time", [("datetime", "2024-09-17T03:30:00Z")])
        assert parser.all_news == []

class TestATagWithJslogHandling:

    @pytest.mark.parametrize("test_attributes,expect_encoded_value", [
        pytest.param([("jslog", "a; b:c; d:e")], "c", id="general"),
        pytest.param([("jslog", "a; b:c-__-_-; d:e")], "c+//+/+", id="Contain base64 safe encoding chars"),
    ])
    @pytest.mark.parametrize("mock_json_decoded_value,expect_url", [
        (["http://a.b.c   "], "http://a.b.c"),
        ([None, None, "   http://a.b.c"], "http://a.b.c"),
        ([None, "   http://a.b.c   "], "http://a.b.c"),
    ])
    def test_handel_starttag(self, test_attributes, expect_encoded_value, mock_json_decoded_value, expect_url):
        with (
            patch.object(_parser.base64, "b64decode", autospec=True) as mock_b64decode,
            patch.object(_parser.json, "loads", autospec=True, return_value=mock_json_decoded_value) as mock_json_loads,
        ):
            parser = _parser.GoogleNewsHTMLParser()
            
            parser.handle_starttag("a", test_attributes)

            assert len(parser._stack) == 1
            actual_article = parser._stack[0]
            assert actual_article.url == expect_url
            assert actual_article.title is None
            assert parser.all_news == []

            mock_b64decode.assert_called_once_with(expect_encoded_value, validate=True)
            mock_json_loads.assert_called_once_with(mock_b64decode.return_value.decode.return_value)

    @pytest.mark.parametrize("test_attributes,expect_encoded_value", [
        pytest.param([("jslog", "a; b:c; d:e")], "c", id="general"),
        pytest.param([("jslog", "a; b:c-__-_-; d:e")], "c+//+/+", id="Contain base64 safe encoding chars"),
    ])
    @pytest.mark.parametrize("mock_json_decoded_value,expect_url", [
        (["http://a.b.c   "], "http://a.b.c"),
        ([None, None, "   http://a.b.c"], "http://a.b.c"),
        ([None, "   http://a.b.c   "], "http://a.b.c"),
    ])
    def test_handel_starttag_article_existing_with_title_only(self, test_attributes, expect_encoded_value, mock_json_decoded_value, expect_url):
        with (
            patch.object(_parser.base64, "b64decode", autospec=True) as mock_b64decode,
            patch.object(_parser.json, "loads", autospec=True, return_value=mock_json_decoded_value) as mock_json_loads,
        ):
            parser = _parser.GoogleNewsHTMLParser()
            parser._stack = [
                GoogleNewsArticle(
                    title="Some Title",
                    url=None,
                )
            ]
            
            parser.handle_starttag("a", test_attributes)

            assert len(parser._stack) == 1
            actual_article = parser._stack[0]
            assert actual_article.url == expect_url
            assert actual_article.title == "Some Title"
            assert parser.all_news == []

            mock_b64decode.assert_called_once_with(expect_encoded_value, validate=True)
            mock_json_loads.assert_called_once_with(mock_b64decode.return_value.decode.return_value)

    def test_handle_starttag_article_existing_with_url(self):
        with (
            patch.object(_parser.base64, "b64decode", autospec=True),
            patch.object(_parser.json, "loads", autospec=True, return_value="asd"),
        ):
            parser = _parser.GoogleNewsHTMLParser()
            parser._stack = [
                GoogleNewsArticle(
                    title="Some Title",
                    url="http://example.com",
                )
            ]
            
            with pytest.raises(RuntimeError):
                parser.handle_starttag("a", [("jslog", "a; b:c; d:e")])
            assert parser.all_news == []

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
    def test_handle_starttag_but_no_url_in_decoded_string(self, mock_json_decoded_value):
        with (
            patch.object(_parser.base64, "b64decode", autospec=True),
            patch.object(_parser.json, "loads", autospec=True, return_value=mock_json_decoded_value),
        ):
            parser = _parser.GoogleNewsHTMLParser()
            
            parser.handle_starttag("a", [("jslog", "a; b:c; d:e")])

            assert len(parser._stack) == 1
            actual_article = parser._stack[0]
            assert actual_article.url is None
            assert actual_article.title is None
            assert parser.all_news == []


    @pytest.mark.parametrize("test_attributes", [
        None,
        [],
        [("a", "v")],
        [("a", "v"), ("d", "e")],
    ])
    def test_handle_starttag_for_a_tag_without_jslog_str(self, test_attributes):
        parser = _parser.GoogleNewsHTMLParser()
        
        parser.handle_starttag("a", test_attributes)

        assert parser._stack == []
        assert parser.all_news == []
        assert not parser._entering_title_a
