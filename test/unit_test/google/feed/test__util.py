import pytest

from unittest.mock import MagicMock, patch

from open_news.google.feed import _util


def _mock_element(tag: str):
    from xml.etree.ElementTree import Element

    mock = MagicMock(spec=Element)
    mock.tag = tag
    return mock


mock_tag1_element = _mock_element("tag1")


@pytest.mark.parametrize("child_elements,test_tag,expect_element", [
    pytest.param(
        [mock_tag1_element],
        "tag1",
        mock_tag1_element,
        id="Single element"
    ),
    pytest.param(
        [mock_tag1_element, _mock_element("tag2")],
        "tag1",
        mock_tag1_element,
        id="2 elements"
    ),
    pytest.param(
        [_mock_element("tag2"), mock_tag1_element],
        "tag1",
        mock_tag1_element,
        id="2 elements on the tail"
    ),
    pytest.param(
        [mock_tag1_element, _mock_element("tag1"), _mock_element("tag1"), _mock_element("tag1")],
        "tag1",
        mock_tag1_element,
        id="2 elements there are matched elements"
    ),
    pytest.param(
        [_mock_element("tag2"), mock_tag1_element, _mock_element("tag1"), _mock_element("tag3"), _mock_element("tag4"), _mock_element("tag5"), _mock_element("tag1")],
        "tag1",
        mock_tag1_element,
        id="2 elements there are matched elements mixed with other tags"
    ),
])
def test_get_element_first_child(child_elements, test_tag, expect_element):
    mock_parent_element = _mock_element("parent_tag")
    mock_parent_element.__getitem__.side_effect = child_elements

    assert _util.get_element_first_child(mock_parent_element, test_tag) is expect_element


@pytest.mark.parametrize("child_elements", [
    [],
    [_mock_element("tag1")],
    [_mock_element("tag1"), _mock_element("tag1"), _mock_element("tag1"), _mock_element("tag1")],
    [_mock_element("tag1"), _mock_element("tag2"), _mock_element("tag3"), _mock_element("tag4")],
])
def test_get_element_first_child_raise_WrongNewsXML_FormatError_if_there_is_no_matched_element(child_elements):
    mock_parent_element = _mock_element("parent_tag")
    mock_parent_element.__getitem__.side_effect = child_elements

    with patch.object(_util.ET, "tostring", autospec=True):
        with pytest.raises(_util.WrongNewsXML_FormatError):
            _util.get_element_first_child(mock_parent_element, "there_is_no_such_tag")
