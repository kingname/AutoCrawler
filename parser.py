"""
通过大模型从HTML中抽取内容
"""
import re
import json
import constants
from llm import LLM
from utils import clean_html


class Parser:
    def __init__(self):
        self.llm = LLM()

    def data_extract(self, html):
        html = clean_html(html)
        msgs = [
            {'role': 'system', 'content': constants.DATA_EXTRACT_SYSTEM},
            {'role': 'user', 'content': html},
        ]
        resp = self.llm.text_chat(msgs)
        if resp.startswith('```'):
            resp = re.search('```json\n(.*)\n```', resp, re.S).group(1)
        return json.loads(resp)

    def paging_extract(self, html):
        html = clean_html(html)
        msgs = [
            {'role': 'system', 'content': constants.PAGING_SYSTEM},
            {'role': 'user', 'content': html},
        ]
        resp = self.llm.text_chat(msgs)
        if resp.startswith('```'):
            resp = re.search('```json\n(.*)\n```', resp, re.S).group(1)
        return json.loads(resp)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    parser = Parser()
    with open('example/listpage.html', 'r') as f:
        html = f.read()
    result = parser.paging_extract(html)
    print(result)
