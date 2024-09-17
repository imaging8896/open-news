import enum


@enum.unique
class Category(enum.Enum):
    TOPICS = "topics"
    ARTICLES = "articles"
    STORIES = "stories"


@enum.unique
class Location(enum.Enum):
    Taiwan = "hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    US = "hl=en-US&gl=US&ceid=US:en"
