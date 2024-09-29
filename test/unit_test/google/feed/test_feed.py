import pytest

from requests import Response
from unittest.mock import patch, MagicMock, call
from xml.etree.ElementTree import Element

from open_news.google import feed


def _mock_element(tag: str):
    mock = MagicMock(spec=Element)
    mock.tag = tag
    return mock


@pytest.fixture
def mock_channel_create():
    with patch.object(feed.GoogleFeedChannel, "create", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_requests_get():
    mock_response = Response()
    with (
        patch.object(feed.requests, "get", autospec=True) as mock,
        patch.object(mock_response, "raise_for_status", autospec=True),
    ):
        mock_response.raw = MagicMock()
        mock.return_value = mock_response
        yield mock


channel_element1 = _mock_element("channel")
channel_element2 = _mock_element("channel")
channel_element3 = _mock_element("channel")


@pytest.fixture
def mock_et_from_string():
    with patch.object(feed.ET, "fromstring", autospec=True) as mock:

        mock.return_value = MagicMock(spec=Element)
        yield mock

@pytest.mark.parametrize("call_args,expect_called_url", [
    pytest.param(
        (feed.Category.ARTICLES, "categort id", feed.Location.Taiwan),
        f"https://news.google.com/rss/{feed.Category.ARTICLES.value}/categort id?{feed.Location.Taiwan.value}",
        id="Without section id",
    ),
    pytest.param(
        (feed.Category.ARTICLES, "categort id", feed.Location.Taiwan, "section id"),
        f"https://news.google.com/rss/{feed.Category.ARTICLES.value}/categort id/sections/section id?{feed.Location.Taiwan.value}",
        id="With section id",
    ),
])
@pytest.mark.parametrize("root_children,expect_elements_tp_create_channel", [
    pytest.param(
        [],
        [],
        id="No any tag"
    ),
    pytest.param(
        [_mock_element("asd")],
        [],
        id="No channel but other tag"
    ),
    pytest.param(
        [_mock_element("asd"), _mock_element("asd1"), _mock_element("asd4"), _mock_element("asd2")],
        [],
        id="No channel but other tags"
    ),
    pytest.param(
        [channel_element1],
        [channel_element1],
        id="1 channel"
    ),
    pytest.param(
        [channel_element1, _mock_element("asd")],
        [channel_element1],
        id="1 channel with other tag"
    ),
    pytest.param(
        [_mock_element("asd1"), channel_element1, _mock_element("asd"), _mock_element("asd2")],
        [channel_element1],
        id="1 channel with other tags"
    ),
    pytest.param(
        [channel_element1, channel_element2, channel_element3],
        [channel_element1, channel_element2, channel_element3],
        id="Channels"
    ),
    pytest.param(
        [channel_element1, _mock_element("asd1"), channel_element2, channel_element3, _mock_element("asd2"), _mock_element("asd3")],
        [channel_element1, channel_element2, channel_element3],
        id="Channels with other tags"
    ),
])
def test_get_feed(call_args, expect_called_url, mock_requests_get, mock_et_from_string, root_children, expect_elements_tp_create_channel, mock_channel_create):
    mock_root_element = mock_et_from_string.return_value
    mock_root_element.__getitem__.side_effect = root_children
    
    channels = feed.get_feed(*call_args)
    assert channels == [
        mock_channel_create.return_value
        for _ in expect_elements_tp_create_channel
    ]

    mock_requests_get.assert_called_once_with(expect_called_url, timeout=10)
    mock_requests_get.return_value.raise_for_status.assert_called_once_with()
    mock_channel_create.assert_has_calls(
        [
            call(element)
            for element in expect_elements_tp_create_channel
        ]
    )
