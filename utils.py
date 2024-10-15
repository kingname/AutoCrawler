from lxml.html import fromstring, HtmlElement
from lxml.html import etree
import constants


def remove_node(node: HtmlElement):
    """
    this is a in-place operation, not necessary to return
    :param node:
    :return:
    """
    parent = node.getparent()
    if parent is not None:
        parent.remove(node)


def clean_html(html):
    selector = fromstring(html)

    for tag in constants.USELESS_TAG:
        eles = selector.xpath(f'//{tag}')
        for ele in eles:
            remove_node(ele)

    html_clean = etree.tostring(selector, pretty_print=True, encoding='unicode')
    return html_clean


def retry(func):
    def wrap(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'Error: {e}')
        return ''
    return wrap
