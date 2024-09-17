import pytest

from unittest.mock import MagicMock, patch

from open_news.google.feed import article
from open_news.google.feed.exception import WrongNewsXML_FormatError


def test_init():
    article.GoogleFeedArticle(title="the title", url="the url", story_url="the story url")


def test_init_without_story_url():
    article.GoogleFeedArticle(title="the title", url="the url")


def test_id_property():
    assert article.GoogleFeedArticle(title="the title", url="the url", story_url="the story url").id == "the url"


@pytest.mark.parametrize("description_text,expect_title,expect_url,expect_story_url", [
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a>&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a></strong>""",
        "壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮",
        "https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5",
        "https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5",
        id="article with story URL",
    ),
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank"></a>&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a></strong>""",
        "",
        "https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5",
        "https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5",
        id="article with empty title with story URL",
    ),
    pytest.param(
        """
        <a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a>&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a></strong>          """,
        "壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮",
        "https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5",
        "https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5",
        id="article with story URL with newline prefix and spaces suffix",
    ),
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiiAJBVV95cUxPQzRTVVFpdzNsTFZYc0pxMEtPZC0tLXRzVmJYaUo4bUphSkxnN2ppN2NXVDlWRFBwOGJZOGRoM3dYZzNFWmVwRmtPdVNnSHh6a3J6c0JVN3NHMFZmcnpXYktubVJud1p3Z0U1TXk4Sjg4RFhPUHB3cTJvZklMRFJ5VUJETjRBOThnU2JCR1BDYTdsQ0VmeDBwT2RWdDRHTFM3bnlBT2tpc2R1OEx2WWVnNXY5MlNGanJBeFkwVkNTOXlvWklJcGU3a0JtY0RuOS1mTk04dEFTaVg4WWpjR2wxWVVEaUEzRGhhZ19TbXB3R2x4SnhISHpZSVRhdm9wcGZvQkh1OGtibUo?oc=5" target="_blank">《熱門族群》融資逆勢增 14檔法人看好</a>&nbsp;&nbsp;<font color="#6f6f6f">Yahoo奇摩股市</font>""",
        "《熱門族群》融資逆勢增 14檔法人看好",
        "https://news.google.com/rss/articles/CBMiiAJBVV95cUxPQzRTVVFpdzNsTFZYc0pxMEtPZC0tLXRzVmJYaUo4bUphSkxnN2ppN2NXVDlWRFBwOGJZOGRoM3dYZzNFWmVwRmtPdVNnSHh6a3J6c0JVN3NHMFZmcnpXYktubVJud1p3Z0U1TXk4Sjg4RFhPUHB3cTJvZklMRFJ5VUJETjRBOThnU2JCR1BDYTdsQ0VmeDBwT2RWdDRHTFM3bnlBT2tpc2R1OEx2WWVnNXY5MlNGanJBeFkwVkNTOXlvWklJcGU3a0JtY0RuOS1mTk04dEFTaVg4WWpjR2wxWVVEaUEzRGhhZ19TbXB3R2x4SnhISHpZSVRhdm9wcGZvQkh1OGtibUo?oc=5",
        None,
        id="article without story URL",
    ),
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiiAJBVV95cUxPQzRTVVFpdzNsTFZYc0pxMEtPZC0tLXRzVmJYaUo4bUphSkxnN2ppN2NXVDlWRFBwOGJZOGRoM3dYZzNFWmVwRmtPdVNnSHh6a3J6c0JVN3NHMFZmcnpXYktubVJud1p3Z0U1TXk4Sjg4RFhPUHB3cTJvZklMRFJ5VUJETjRBOThnU2JCR1BDYTdsQ0VmeDBwT2RWdDRHTFM3bnlBT2tpc2R1OEx2WWVnNXY5MlNGanJBeFkwVkNTOXlvWklJcGU3a0JtY0RuOS1mTk04dEFTaVg4WWpjR2wxWVVEaUEzRGhhZ19TbXB3R2x4SnhISHpZSVRhdm9wcGZvQkh1OGtibUo?oc=5" target="_blank"></a>&nbsp;&nbsp;<font color="#6f6f6f">Yahoo奇摩股市</font>""",
        "",
        "https://news.google.com/rss/articles/CBMiiAJBVV95cUxPQzRTVVFpdzNsTFZYc0pxMEtPZC0tLXRzVmJYaUo4bUphSkxnN2ppN2NXVDlWRFBwOGJZOGRoM3dYZzNFWmVwRmtPdVNnSHh6a3J6c0JVN3NHMFZmcnpXYktubVJud1p3Z0U1TXk4Sjg4RFhPUHB3cTJvZklMRFJ5VUJETjRBOThnU2JCR1BDYTdsQ0VmeDBwT2RWdDRHTFM3bnlBT2tpc2R1OEx2WWVnNXY5MlNGanJBeFkwVkNTOXlvWklJcGU3a0JtY0RuOS1mTk04dEFTaVg4WWpjR2wxWVVEaUEzRGhhZ19TbXB3R2x4SnhISHpZSVRhdm9wcGZvQkh1OGtibUo?oc=5",
        None,
        id="article with empty title without story URL",
    ),
    pytest.param(
        """      <a href="https://news.google.com/rss/articles/CBMiiAJBVV95cUxPQzRTVVFpdzNsTFZYc0pxMEtPZC0tLXRzVmJYaUo4bUphSkxnN2ppN2NXVDlWRFBwOGJZOGRoM3dYZzNFWmVwRmtPdVNnSHh6a3J6c0JVN3NHMFZmcnpXYktubVJud1p3Z0U1TXk4Sjg4RFhPUHB3cTJvZklMRFJ5VUJETjRBOThnU2JCR1BDYTdsQ0VmeDBwT2RWdDRHTFM3bnlBT2tpc2R1OEx2WWVnNXY5MlNGanJBeFkwVkNTOXlvWklJcGU3a0JtY0RuOS1mTk04dEFTaVg4WWpjR2wxWVVEaUEzRGhhZ19TbXB3R2x4SnhISHpZSVRhdm9wcGZvQkh1OGtibUo?oc=5" target="_blank">《熱門族群》融資逆勢增 14檔法人看好</a>&nbsp;&nbsp;<font color="#6f6f6f">Yahoo奇摩股市</font>
        
        """,
        "《熱門族群》融資逆勢增 14檔法人看好",
        "https://news.google.com/rss/articles/CBMiiAJBVV95cUxPQzRTVVFpdzNsTFZYc0pxMEtPZC0tLXRzVmJYaUo4bUphSkxnN2ppN2NXVDlWRFBwOGJZOGRoM3dYZzNFWmVwRmtPdVNnSHh6a3J6c0JVN3NHMFZmcnpXYktubVJud1p3Z0U1TXk4Sjg4RFhPUHB3cTJvZklMRFJ5VUJETjRBOThnU2JCR1BDYTdsQ0VmeDBwT2RWdDRHTFM3bnlBT2tpc2R1OEx2WWVnNXY5MlNGanJBeFkwVkNTOXlvWklJcGU3a0JtY0RuOS1mTk04dEFTaVg4WWpjR2wxWVVEaUEzRGhhZ19TbXB3R2x4SnhISHpZSVRhdm9wcGZvQkh1OGtibUo?oc=5",
        None,
        id="article without story URL with spaces prefix and newline suffix",
    ),
])
def test_create_from_description_with_story(description_text, expect_title, expect_url, expect_story_url):
    articles = article.GoogleFeedArticle.create_from_description_with_story(description_text)
    
    assert isinstance(articles, list)
    assert len(articles) == 1
    
    the_article = articles[0]
    assert the_article.title == expect_title
    assert the_article.url == expect_url
    assert the_article.story_url == expect_story_url


@pytest.mark.parametrize("description_text", ["", "a", "<b", "    a", """
<b""", """
"""])
def test_create_from_description_with_story_raise_WrongNewsXML_FormatError_if_description_not_start_with_an_a_link(description_text):
    with pytest.raises(WrongNewsXML_FormatError):
        article.GoogleFeedArticle.create_from_description_with_story(description_text)


@pytest.mark.parametrize("description_text", [
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a><a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a>&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a></strong>""",
        id="2 article URLs with story URL",
    ),
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a><a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a><a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a><a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a>&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a></strong>""",
        id="4 article URLs with story URL",
    ),
    pytest.param(
        """&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a></strong>""",
        id="No article URL with story URL",
    ),
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a><a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a>&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong></strong>""",
        id="2 article URLs without story URL",
    ),
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a><a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a><a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a><a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">壽險公司控管風險 實支實付健康險「非保證續保」恐成新風潮</a>&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong></strong>""",
        id="4 article URLs without story URL",
    ),
    pytest.param(
        """&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong></strong>""",
        id="No article URL without story URL",
    ),
])
def test_create_from_description_with_story_raise_WrongNewsXML_FormatError_if_there_is_not_just_1_article_url(description_text):
    with pytest.raises(WrongNewsXML_FormatError):
        article.GoogleFeedArticle.create_from_description_with_story(description_text)


@pytest.mark.parametrize("description_text", [
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5" target="_blank">123</a><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a>&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a></strong>""",
        id="article with 3 story URLs",
    ),
    pytest.param(
        """&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a></strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a>""",
        id="No article URL with 2 story URLs",
    ),
])
def test_create_from_description_with_story_raise_WrongNewsXML_FormatError_if_there_are_more_than_1_story_url(description_text):
    with pytest.raises(WrongNewsXML_FormatError):
        article.GoogleFeedArticle.create_from_description_with_story(description_text)


@pytest.mark.parametrize("description_text", [
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5"&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5"</strong>""",
        id="No any title",
    ),
    pytest.param(
        """<a href="https://news.google.com/rss/articles/CBMiUEFVX3lxTE5Hb2Y2dXdxbzhKV0lnaVEtUGhMYl9tUnVQZ2VWZWlFZmRRbWJST1I1RmRzQmRXRUpQR25QNnJkc3k2bG1leDAwS3lQdkpXUWpJ0gFWQVVfeXFMT1d5WklIWFZ4UEN2aVBmbkFMaTVodlRTV1hud0dtVkpmUkN0WXFJNE9zNndUZkpzdFRzS3JhUXlDODhnV1FnMWd2R0h3d041R1U3WFJFbWc?oc=5"&nbsp;&nbsp;<font color="#6f6f6f">聯合新聞網</font><strong><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkalp1ZkRCSHdwSHVYeEp0dTVTZ0FQAQ?hl=zh-TW&gl=TW&ceid=TW:zh-Hant&oc=5" target="_blank">前往 Google 新聞查看完整報導</a></strong>""",
        id="No article URL with story URL",
    ),
])
def test_create_from_description_with_story_raise_WrongNewsXML_FormatError_if_there_is_no_title(description_text):
    with pytest.raises(WrongNewsXML_FormatError):
        article.GoogleFeedArticle.create_from_description_with_story(description_text)


@pytest.mark.parametrize("description_text,expect_articles", [
    pytest.param(
        """<ol><li><a href="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5" target="_blank">EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲</a>&nbsp;&nbsp;<font color="#6f6f6f">Anue鉅亨</font></li><li><a href="https://news.google.com/rss/articles/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5" target="_blank">美歐基本面相近 美滙弱勢宜謹慎</a>&nbsp;&nbsp;<font color="#6f6f6f">趨勢</font></li><li><a href="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5" target="_blank">【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網</a>&nbsp;&nbsp;<font color="#6f6f6f">香港文匯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5" target="_blank">法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投</a>&nbsp;&nbsp;<font color="#6f6f6f">富聯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5" target="_blank">市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights</a>&nbsp;&nbsp;<font color="#6f6f6f">Investing.com 香港</font></li></ol>""",
        [
            article.GoogleFeedArticle(title="EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲", url="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5"),
            article.GoogleFeedArticle(title="美歐基本面相近 美滙弱勢宜謹慎", url="https://news.google.com/rss/articles/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5"),
            article.GoogleFeedArticle(title="【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網", url="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5"),
            article.GoogleFeedArticle(title="法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投", url="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5"),
            article.GoogleFeedArticle(title="市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights", url="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5"),
        ],
        id="articles",
    ),
    pytest.param(
        """<ol><li><a href="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5" target="_blank">EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲</a>&nbsp;&nbsp;<font color="#6f6f6f">Anue鉅亨</font></li><li><a href="https://news.google.com/rss/articles/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5" target="_blank"></a>&nbsp;&nbsp;<font color="#6f6f6f">趨勢</font></li><li><a href="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5" target="_blank">【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網</a>&nbsp;&nbsp;<font color="#6f6f6f">香港文匯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5" target="_blank">法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投</a>&nbsp;&nbsp;<font color="#6f6f6f">富聯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5" target="_blank"></a>&nbsp;&nbsp;<font color="#6f6f6f">Investing.com 香港</font></li></ol>""",
        [
            article.GoogleFeedArticle(title="EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲", url="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5"),
            article.GoogleFeedArticle(title="", url="https://news.google.com/rss/articles/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5"),
            article.GoogleFeedArticle(title="【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網", url="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5"),
            article.GoogleFeedArticle(title="法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投", url="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5"),
            article.GoogleFeedArticle(title="", url="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5"),
        ],
        id="articles with empty title",
    ),
    pytest.param(
        """
        
        <ol><li><a href="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5" target="_blank">EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲</a>&nbsp;&nbsp;<font color="#6f6f6f">Anue鉅亨</font></li><li><a href="https://news.google.com/rss/articles/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5" target="_blank">美歐基本面相近 美滙弱勢宜謹慎</a>&nbsp;&nbsp;<font color="#6f6f6f">趨勢</font></li><li><a href="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5" target="_blank">【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網</a>&nbsp;&nbsp;<font color="#6f6f6f">香港文匯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5" target="_blank">法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投</a>&nbsp;&nbsp;<font color="#6f6f6f">富聯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5" target="_blank">市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights</a>&nbsp;&nbsp;<font color="#6f6f6f">Investing.com 香港</font></li></ol>    """,
        [
            article.GoogleFeedArticle(title="EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲", url="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5"),
            article.GoogleFeedArticle(title="美歐基本面相近 美滙弱勢宜謹慎", url="https://news.google.com/rss/articles/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5"),
            article.GoogleFeedArticle(title="【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網", url="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5"),
            article.GoogleFeedArticle(title="法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投", url="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5"),
            article.GoogleFeedArticle(title="市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights", url="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5"),
        ],
        id="articles with newline prefix and spaces suffix",
    ),
])
def test_create_from_description_with_stories(description_text, expect_articles):
    articles = article.GoogleFeedArticle.create_from_description_with_stories(description_text)
    
    assert isinstance(articles, list)
    assert len(articles) == len(expect_articles)

    for actual_article, expect_article in zip(articles, expect_articles):
        assert actual_article.title == expect_article.title
        assert actual_article.url == expect_article.url
        assert actual_article.story_url == expect_article.story_url
        assert actual_article.story_url is None


@pytest.mark.parametrize("description_text", ["", """
     """, "<ol", "<a>", "<a"])
def test_create_from_description_with_stories_raise_WrongNewsXML_FormatError_if_not_start_with_ol_tag(description_text):
    with pytest.raises(WrongNewsXML_FormatError):
        article.GoogleFeedArticle.create_from_description_with_stories(description_text)


@pytest.mark.parametrize("description_text", [
    pytest.param(
        """<ol><li><a href="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5" target="_blank">EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲</a>&nbsp;&nbsp;<font color="#6f6f6f">Anue鉅亨</font></li><li><a href="https://news.google.com/rss/stories/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5" target="_blank">美歐基本面相近 美滙弱勢宜謹慎</a>&nbsp;&nbsp;<font color="#6f6f6f">趨勢</font></li><li><a href="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5" target="_blank">【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網</a>&nbsp;&nbsp;<font color="#6f6f6f">香港文匯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5" target="_blank">法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投</a>&nbsp;&nbsp;<font color="#6f6f6f">富聯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5" target="_blank">市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights</a>&nbsp;&nbsp;<font color="#6f6f6f">Investing.com 香港</font></li></ol>""",
        id="1 story URL",
    ),
    pytest.param(
        """<ol><li><a href="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5" target="_blank">EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲</a>&nbsp;&nbsp;<font color="#6f6f6f">Anue鉅亨</font></li><li><a href="https://news.google.com/rss/stories/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5" target="_blank">美歐基本面相近 美滙弱勢宜謹慎</a>&nbsp;&nbsp;<font color="#6f6f6f">趨勢</font></li><li><a href="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5" target="_blank">【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網</a>&nbsp;&nbsp;<font color="#6f6f6f">香港文匯網</font></li><li><a href="https://news.google.com/rss/stories/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5" target="_blank">法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投</a>&nbsp;&nbsp;<font color="#6f6f6f">富聯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5" target="_blank">市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights</a>&nbsp;&nbsp;<font color="#6f6f6f">Investing.com 香港</font></li></ol>""",
        id="Story URLs",
    ),
])
def test_create_from_description_with_stories_raise_WrongNewsXML_FormatError_if_there_is_story_url(description_text):
    with pytest.raises(WrongNewsXML_FormatError):
        article.GoogleFeedArticle.create_from_description_with_stories(description_text)


@pytest.mark.parametrize("description_text", [
    pytest.param(
        """<ol><li><a target="_blank">EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲</a>&nbsp;&nbsp;<font color="#6f6f6f">Anue鉅亨</font></li><li><a href="https://news.google.com/rss/articles/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5" target="_blank">美歐基本面相近 美滙弱勢宜謹慎</a>&nbsp;&nbsp;<font color="#6f6f6f">趨勢</font></li><li><a href="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5" target="_blank">【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網</a>&nbsp;&nbsp;<font color="#6f6f6f">香港文匯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5" target="_blank">法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投</a>&nbsp;&nbsp;<font color="#6f6f6f">富聯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5" target="_blank">市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights</a>&nbsp;&nbsp;<font color="#6f6f6f">Investing.com 香港</font></li></ol>""",
        id="Missing 1 article URL",
    ),
    pytest.param(
        """<ol><a href="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5" target="_blank">EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲</a>&nbsp;&nbsp;<font color="#6f6f6f">Anue鉅亨</font></li><li><a href="https://news.google.com/rss/stories/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5" target="_blank">美歐基本面相近 美滙弱勢宜謹慎</a>&nbsp;&nbsp;<font color="#6f6f6f">趨勢</font></li><li><a href="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5" target="_blank">【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網</a>&nbsp;&nbsp;<font color="#6f6f6f">香港文匯網</font></li><li><a href="https://news.google.com/rss/stories/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5" target="_blank">法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投</a>&nbsp;&nbsp;<font color="#6f6f6f">富聯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5" target="_blank">市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights</a>&nbsp;&nbsp;<font color="#6f6f6f">Investing.com 香港</font></li></ol>""",
        id="Additional 1 article URL",
    ),
])
def test_create_from_description_with_stories_raise_WrongNewsXML_FormatError_if_article_urls_not_match_expect_count(description_text):
    with pytest.raises(WrongNewsXML_FormatError):
        article.GoogleFeedArticle.create_from_description_with_stories(description_text)

@pytest.mark.parametrize("description_text", [
    pytest.param(
        """<ol><li><a href="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5" </a>&nbsp;&nbsp;<font color="#6f6f6f">Anue鉅亨</font></li><li><a href="https://news.google.com/rss/articles/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5" target="_blank">美歐基本面相近 美滙弱勢宜謹慎</a>&nbsp;&nbsp;<font color="#6f6f6f">趨勢</font></li><li><a href="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5" target="_blank">【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網</a>&nbsp;&nbsp;<font color="#6f6f6f">香港文匯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5" target="_blank">法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投</a>&nbsp;&nbsp;<font color="#6f6f6f">富聯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5" target="_blank">市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights</a>&nbsp;&nbsp;<font color="#6f6f6f">Investing.com 香港</font></li></ol>""",
        id="Missing 1 title",
    ),
    pytest.param(
        """<ol><li><a href="https://news.google.com/rss/articles/CBMiT0FVX3lxTE5DVlA5a19RbDRJZ1l0VVJObHhRMldIeEM1QUZNWWVQeXFteTl0dkQ4b19ZNlNtZy1CczBzVVVRb0hZQ0xkVVduQlowX3VJQjQ?oc=5" target="_blank">EUR/USD：全球市場進入緊張的九月，美元兌歐元上漲</a>target="_blank">EUR/USD：全球市場進入緊張的九月，dasda美元兌歐元上漲</a>&nbsp;&nbsp;<font color="#6f6f6f">Anue鉅亨</font></li><li><a href="https://news.google.com/rss/articles/CBMigwJBVV95cUxQWE1PMmFBZEhieE9jcXpKQ01Bem5LcEFRZ3hNQ3YzN1RYa0l5b1BqWVIwaExZYThiOHdUM19xWFkxOVJsN3V3V2YxV0ZOYjg5blc4djlMa25mXzJqbkx1NjJHNVFEblRtbXRscDE4emtNY1J4N0dPbDBNNFZGWkJZZWhRY3VSVndKc1BmbDh4cWl1UnpKZGw2cmgtc084VmEyaWtJNGFZLVdpeHYtVVdHdGIzdFBtVEtPSFVmcTZwTnAzUGtlZFlpUWgyRFRiLWxWZ2QxRlpmLW5lcDdLY25HVlBCUlVxVFRpN0xtTEVoTTVCd2NSb0ZKMUNqVkRSdVltNng4?oc=5" target="_blank">美歐基本面相近 美滙弱勢宜謹慎</a>&nbsp;&nbsp;<font color="#6f6f6f">趨勢</font></li><li><a href="https://news.google.com/rss/articles/CBMid0FVX3lxTFBGQXRGTm9IZlhUUDNWelJsRkhyNkJyeFY2RU1URnpDY3JOQm9aWTlVMGRoSDFTeUZSRHh5Z1pWRGdyWXZ5SzdFYWhNM2EyX0haVGNNMGJ3c0Q5cTN3R3l1dTdMMEdCN0tEM3hhUTE2NUlZQmllLXRV?oc=5" target="_blank">【金匯動向】靜候美非農數據歐元跌幅放緩- 財經 - 香港文匯網</a>&nbsp;&nbsp;<font color="#6f6f6f">香港文匯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiiAFBVV95cUxPeFJVTGRqT2pnc29yemFwSmhOWUUyVENGcGt3UFZTZ182ZlllTmM3S1lBVmF1NXViajFVaUZlaE5NNFZNdzZMRWtQTDhUZzNXb1RqbGxQTXhfRDUyVzVSM1dFVTRGbmhmTFNJVE1udWdPVTJtUlNKRkkxa0ctY1V3dkdwTjdKNGFw?oc=5" target="_blank">法人觀點：ECB利率路徑不確定性，Saxo估歐元兌美元近期1.08-1.12美元區間交投</a>&nbsp;&nbsp;<font color="#6f6f6f">富聯網</font></li><li><a href="https://news.google.com/rss/articles/CBMiZkFVX3lxTE1VM1owRFhQVFpSdy1teHRDekxjMnQxQm0ycFcxTDZIdVl6ay1fYWZ1WlJwRkxJV2dmWl9WdUZEZExCRDNvOFVEX3loSWYxQzhIZkE2VmVoNHZsczRrcm10aVFpSHI1UQ?oc=5" target="_blank">市場聚焦美國8月非農數據 歐元兌美元或延續三連漲 作者 投資慧眼Insights</a>&nbsp;&nbsp;<font color="#6f6f6f">Investing.com 香港</font></li></ol>""",
        id="Additional 1 title",
    ),
])
def test_create_from_description_with_stories_raise_WrongNewsXML_FormatError_if_titles_not_match_expect_count(description_text):
    with pytest.raises(WrongNewsXML_FormatError):
        article.GoogleFeedArticle.create_from_description_with_stories(description_text)
