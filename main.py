import datetime

import httpx

import constants
import pymongo
from utils import retry
from collections import deque
from urllib.parse import urljoin
from lxml.html import fromstring
from parser import Parser
from dotenv import load_dotenv


load_dotenv()


class AutoCrawler:
    def __init__(self):
        self.parser = Parser()
        self.handler = pymongo.MongoClient().autocrawler.detail
        self.detail_rule_cache = None

    @retry
    def get(self, url):
        print(f'正在抓取：{url}')
        with httpx.Client(headers=constants.HEADERS, timeout=10, follow_redirects=True) as client:
            response = client.get(url)
            return response.text

    def extract_detail(self, detail_rule, html):
        selector = fromstring(html)
        result = {}
        for rule in detail_rule:
            xpath = rule['xpath']
            last_part = xpath.split('/')[-1]
            if last_part.startswith('@'):
                field_name = rule['field_name']
                value = selector.xpath(xpath)
                result[field_name] = value[0] if value else ''
            elif last_part == 'text()':
                field_name = rule['field_name']
                value = selector.xpath(xpath)
                result[field_name] = ''.join(value).strip()
            else:
                xpath = f'{xpath}/text()'
                field_name = rule['field_name']
                value = selector.xpath(xpath)
                result[field_name] = ''.join(value).strip()
        return result

    def crawl(self, base_url, page_num=1, cache_detail_rule=True):
        target = deque([{'page_type': 'list', 'url': base_url}])
        current_page = 0
        while target:
            target_item = target.popleft()
            url = target_item['url']
            html = self.get(url)
            if not html:
                continue
            if target_item['page_type'] == 'detail' and cache_detail_rule and self.detail_rule_cache:
                info = self.detail_rule_cache
            else:
                info = self.parser.data_extract(html)
            if not info:
                break
            page_type = info['page_type']
            if page_type == 'list':
                current_page += 1
                for field in info['articles']:
                    title = field['title']
                    detail_url = urljoin(url, field['url']) if not field['url'].startswith('http') else field['url']
                    print(f'发现详情页：{title} {detail_url}')
                    target.append({'page_type': 'detail', 'url': detail_url})
                if current_page < page_num:
                    pagination = self.parser.paging_extract(html)
                    next_url = pagination.get('url')
                    if not next_url:
                        break
                    target.append({'page_type': 'list', 'url': urljoin(url, next_url)})
            elif page_type == 'detail':
                detail_rule = info['fields']
                doc = self.extract_detail(detail_rule, html)
                doc['url'] = url
                doc['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.handler.insert_one(doc)
                if not self.detail_rule_cache:
                    self.detail_rule_cache = info


if __name__ == '__main__':
    crawler = AutoCrawler()
    crawler.crawl('https://kingname.info/archives/', 3, cache_detail_rule=True)
