import re

from .exception import WrongNewsXML_FormatError
from ..article import GoogleNewsArticle


class GoogleFeedArticle(GoogleNewsArticle):
    
    @classmethod
    def create_from_description_with_story(clz, description_text: str):
        description_text = description_text.strip()
        
        if not description_text.startswith("<a"):
            raise WrongNewsXML_FormatError(f"Should start with '<a' for single story article\n{description_text}")
        
        article_urls, story_url = _get_article_urls(description_text)
        
        if len(article_urls) != 1:
            raise WrongNewsXML_FormatError(f"Should contain 1 article URL. Got {article_urls}\n{description_text}")
        article_url = article_urls[0]

        titles = _get_article_titles(description_text)
        if not titles or (len(titles) == 1 and story_url is not None):
            raise WrongNewsXML_FormatError(f"Should contain title\n{description_text}")
        
        return [clz(title=titles[0], url=article_url, story_url=story_url)]
    
    @classmethod
    def create_from_description_with_stories(clz, description_text: str):
        description_text = description_text.strip()

        if not description_text.startswith("<ol>"):
            raise WrongNewsXML_FormatError(f"Should start with '<ol>' for stories article\n{description_text}")
        
        expect_article_count = description_text.count("<li")

        article_urls, story_url = _get_article_urls(description_text)

        if story_url is not None:
            raise WrongNewsXML_FormatError(f"Should contain no story URL for articles. Got {story_url}\n{description_text}")

        if len(article_urls) != expect_article_count:
            raise WrongNewsXML_FormatError(f"Should contain {expect_article_count} URLs\n{description_text}")
        
        titles = _get_article_titles(description_text)
        if len(titles) != expect_article_count:
            raise WrongNewsXML_FormatError(f"Should contain {expect_article_count} titles\n{description_text}")

        return [
            clz(title=title, url=article_url)
            for title, article_url in zip(titles, article_urls)
        ]
    

def _get_article_urls(description_text: str) -> tuple[list[str], str | None]:
    urls = re.findall(r"href=\"(https.+?)\"", description_text)
    
    article_urls = [x for x in urls if "/articles/" in x]
    story_urls = [x for x in urls if "/stories/" in x]
    if len(story_urls) == 0:
        return article_urls, None
    elif len(story_urls) == 1:
        return article_urls, story_urls[0]
    else:
        raise WrongNewsXML_FormatError(f"Should contain only 1 story URL\n{description_text}")


def _get_article_titles(description_text: str) -> list[str]:
    return re.findall(r"_blank\">(.*?)<\/a>", description_text)
