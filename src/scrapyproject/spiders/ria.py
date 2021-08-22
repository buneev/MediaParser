# -*- coding:utf-8 -*-

# created 08.11.2019

from scrapy import Request
from scrapy.selector import Selector
from scrapy import signals
from scrapy import Spider
from scrapyproject.helpers.base import BaseSpider
from scrapyproject.helpers.help_func import *
import json


# main page xpath
ART_BLOCK = "//div[contains(@class, 'cell-list__item ')]"
ART_URL = "//a/@href"

# article page xpath
P_ART_BLOCK = "//div[@class='layout-article']"
P_ART_CODE = "//@data-article-id"
P_ART_TITLE = "//h1[@class='article__title']/text()"
P_ART_TEXT = "//div[@class='article__block' and @data-type='text']"
P_ART_IMG = "//div[@class='photoview__open']/@data-photoview-src"
P_ART_DATE = "//div[@class='article__info-date']/a/text()"
P_ART_AUTHOR = ""


class ParseFunc(BaseSpider):

    def get_art_urls(self, response):
        items = response.xpath(ART_BLOCK).extract()
        urls = [Selector(text=i).xpath(ART_URL).extract_first(default='') for i in items]
        return urls

    def get_code(self, article):
        code = article.xpath(P_ART_CODE).extract_first(default='')
        return {"code": code}

    def get_title(self, article):
        title = article.xpath(P_ART_TITLE).extract_first(default='')
        return {"title": title}

    def get_text(self, article):
        text = article.xpath(P_ART_TEXT).extract()
        text = list(map(lambda x: clear_str(x), text))
        text = " ".join(text)
        return {"text": text}
    
    def get_images(self, article):
        imgs = article.xpath(P_ART_IMG).extract()
        return {"image": imgs[0]}

    def get_date(self, article):
        date = article.xpath(P_ART_DATE).extract_first(default='')
        if date:
            date = date.strip().split()
            date = '{} {}'.format(date[1], date[0])
        return {"pub_date": date}


class RiaSpider(ParseFunc):
    name = "ria"
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1.1,
        'DOWNLOAD_TIMEOUT': 40,
    }
    start_urls = [
        "https://ria.ru/",
    ]

    def parse(self, response):
        art_urls = self.get_art_urls(response)
        for url in art_urls:
            yield Request(url=url, callback=self.parse_article)

    def parse_article(self, response):
        result = self.get_art_structure()
        first_art_on_page = response.xpath(P_ART_BLOCK).extract_first(default='')
        article = Selector(text=first_art_on_page)
        result['sourse_link'] = response.url
        try:
            result.update(self.get_code(article))
            result.update(self.get_title(article))
            result.update(self.get_text(article))
            result.update(self.get_images(article))
            result.update(self.get_date(article))
            yield result
        except Exception as err:
            self.logger.error(f"Error in parse article: '{err}'")
