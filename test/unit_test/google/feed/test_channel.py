import pytest

from unittest.mock import MagicMock, patch, call
from datetime import datetime

from open_news.google.feed import channel


@pytest.fixture
def mock_get_element_first_child():
    with patch.object(channel, "get_element_first_child", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_item_create():
    with patch.object(channel.GoogleFeedItem, "create", autospec=True) as mock:
        yield mock


MOCK_DATETIME_STR = "Fri, 06 Sep 2024 00:12:25 GMT"
MOCK_DATETIME = datetime(year=2024, month=9, day=6, hour=0, minute=12, second=25)


def _mock_element():
    from xml.etree.ElementTree import Element

    mock = MagicMock(spec=Element)
    return mock


def test_create(mock_get_element_first_child: MagicMock, mock_item_create: MagicMock):
    mock_element1 = _mock_element()
    mock_element1.tag = "item"
    mock_element2 = _mock_element()
    mock_element2.tag = "not_item"
    mock_element3 = _mock_element()
    mock_element3.tag = "item"
    mock_element4 = _mock_element()
    mock_element4.tag = "item"
    mock_element5 = _mock_element()
    mock_element5.tag = "not_item"
    
    mock_root_element = _mock_element()
    mock_root_element.__getitem__.side_effect = [mock_element1, mock_element2, mock_element3, mock_element4, mock_element5]

    def _mock_get_element_first_child_side_effect(the_element, tag: str):
        assert the_element is mock_root_element
        
        if tag == "lastBuildDate":
            element = _mock_element()
            element.text = MOCK_DATETIME_STR
            return element

    mock_get_element_first_child.side_effect = _mock_get_element_first_child_side_effect

    the_channel = channel.GoogleFeedChannel.create(mock_root_element)

    assert the_channel.update_time == MOCK_DATETIME
    assert the_channel.items == [
        mock_item_create.return_value,
        mock_item_create.return_value,
        mock_item_create.return_value,
    ]
    mock_item_create.assert_has_calls(
        [
            call(mock_element1),
            call(mock_element3),
            call(mock_element4),
        ]
    )
