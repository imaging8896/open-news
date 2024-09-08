from xml.etree.ElementTree import Element
from datetime import datetime
from dataclasses import dataclass

from ._util import get_element_first_child, TIME_FORMAT
from .item import GoogleFeedItem


@dataclass(frozen=True, slots=True, kw_only=True)
class GoogleFeedChannel:
    update_time: datetime
    items: list[GoogleFeedItem]

    @classmethod
    def create(clz, channel: Element):
        return clz(
            update_time=datetime.strptime(get_element_first_child(channel, "lastBuildDate").text.strip(), TIME_FORMAT),
            items=[
                GoogleFeedItem.create(child) 
                for child in channel
                if child.tag == "item"
            ],
        )
