from scrapy import Spider
from scrapy import signals
from copy import deepcopy
from datetime import datetime
import requests
import json

BLOG_URL = 'http://127.0.0.1:8000'

HEADERS = {
    'Content-Type': 'application/json',
}

class BaseSpider(Spider):
    dest_url = f'{BLOG_URL}/article/api/'

    def __init__(self, spider_name):
        self.articles = list()

    @classmethod
    def from_crawler(cls, crawler):
        
        # instantiate the extension object
        ext = cls(crawler.spidercls.name)
        # ext = cls(dest_url, crawler.spidercls.name)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        
        # return the extension object
        return ext

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s", spider.name)

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        if len(self.articles) > 0:
            self.send_scraped_data(self.articles, spider)

    def item_scraped(self, item, spider):
        self.articles.append(deepcopy(item))

    def send_scraped_data(self, articles=None, spider=None):
        spider.logger.info(f"Spider '{spider.name}' ends work, request to: {self.dest_url}")
        try:
            data = json.dumps(articles)
            r = requests.post(url=self.dest_url, headers=HEADERS, data=data)
            if r.status_code == 200:
                spider.logger.info("Data sent successful")
            elif r.status_code == 201:
                spider.logger.info(f"Created. status_code: {r.status_code}. {r.text}")
            else:
                spider.logger.info(f"Bad response. status_code: {r.status_code}. {r.text}")
        except json.JSONDecodeError:
            spider.logger.info("Error encode items to json")

    def get_art_structure(self):
        result = {
            "sourse_link": "",
            "code": "",
            "title": "",
            "text": "",
            "image": "",
            "pub_date": "",
            "author": "",
            "tags": [],
        }
        return result
