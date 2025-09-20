from unittest.mock import patch, MagicMock, ANY

import pytest

from open_news import google


@pytest.fixture
def mock_requests_get():
    with patch("open_news.google.request_get", autospec=True) as mock:
        yield mock


@pytest.mark.parametrize("call_args,expect_called_url", [
    pytest.param(
        (google.Category.ARTICLES, "categort id", google.Location.Taiwan),
        f"https://news.google.com/{google.Category.ARTICLES.value}/categort id?{google.Location.Taiwan.value}",
        id="Without section id",
    ),
    pytest.param(
        (google.Category.ARTICLES, "categort id", google.Location.Taiwan, "section id"),
        f"https://news.google.com/{google.Category.ARTICLES.value}/categort id/sections/section id?{google.Location.Taiwan.value}",
        id="With section id",
    ),
])
def test_get_news(call_args, expect_called_url, mock_requests_get):
    with patch.object(google, "GoogleNewsHTMLParser", autospec=True) as mock_parser_class:
        mock_parser_class.return_value.all_news = MagicMock()

        assert google.get_news(*call_args) == mock_parser_class.return_value.all_news

        mock_requests_get.assert_called_once_with(expect_called_url, timeout=10)
        mock_parser_class.return_value.feed.assert_called_once_with(mock_requests_get.return_value)
