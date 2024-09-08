import xml.etree.ElementTree as ET

from xml.etree.ElementTree import Element

from .exception import WrongNewsXML_FormatError


TIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"


def get_element_first_child(parent: Element, child_tag: str) -> Element:
    for child in parent:
        if child.tag == child_tag:
            return child
    raise WrongNewsXML_FormatError(f"No '{child_tag}' tag under\n{ET.tostring(parent, encoding='unicode')}")
