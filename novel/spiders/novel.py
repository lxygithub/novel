# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     novel
   Description :
   Author :       59432
   date：          2019/11/10
-------------------------------------------------
   Change Activity:
                   2019/11/10:
-------------------------------------------------
"""
import copy
import re

import scrapy
from scrapy import Request, Selector

from novel.items import NovelItem

__author__ = '59432'


class Novel(scrapy.Spider):
    name = 'novel'
    base_url = 'http://www.quanben.io'
    pattern_more_url = re.compile("jsonp&callback=(.*?)&pinyin=")
    pattern_more_content_json = re.compile("content\":\"(.*?)\"}\);")

    def start_requests(self):
        yield Request(self.base_url, callback=self.parse_type)

    def parse_type(self, response):
        page = response.selector

        type_urls = page.xpath('//div[@class="nav"]/a')
        dom_types = page.xpath('//div[@class="nav"]/a/span')
        # type_urls = page.xpath('//div[@class="nav"]/a')[:1]
        # dom_types = page.xpath('//div[@class="nav"]/a/span')[:1]

        for dom_type, dom_type_url in zip(dom_types, type_urls):
            type_url = self.base_url + dom_type_url.xpath('@href').get()
            type_name = dom_type.xpath('text()').get()

            yield Request(type_url, callback=self.parse_total_pages, meta={'type_name': type_name})

    def parse_total_pages(self, response):
        type_name = response.meta["type_name"]
        type_url = response.url
        page = response.selector

        current_page_txt = page.xpath('//span[@class="cur_page"]/text()').get()

        total_page = int(current_page_txt.split('/')[1].strip())
        for i in range(1, total_page + 1):
            # for i in range(1, 2):
            yield Request(type_url.replace('.html', str('_%d.html' % i)), callback=self.parse_per_page,
                          meta={'type_name': type_name})

    def parse_per_page(self, response):
        type_name = response.meta["type_name"]
        page = response.selector

        selector_books = page.xpath('//div[@class="list2"]')

        for selector_book in selector_books:
            book_thumb = selector_book.xpath('//img/@src').get()
            book_name = selector_book.xpath('//img/@alt').get()
            book_url = self.base_url + selector_book.xpath('//h3/a[@itemprop="url"]/@href').get()
            book_list_url = book_url + "list.html"
            book_author = selector_book.xpath('//span[@itemprop="author"]/text()').get()
            book_desc = selector_book.xpath('//p[@itemprop="description"]/text()').get()
            yield Request(book_list_url, callback=self.parse_chapters,
                          meta={'type_name': type_name,
                                'book_name': book_name,
                                'book_url': book_url,
                                'book_thumb': book_thumb,
                                'book_author': book_author,
                                'book_desc': book_desc,
                                })

    def parse_chapters(self, response):
        page = response.selector
        book_chapters = page.xpath('//ul[@class="list3"]/li')
        # book_chapters = page.xpath('//ul[@class="list3"]/li')[:3]

        for book_chapter in book_chapters:
            chapter_url = self.base_url + book_chapter.xpath('.//a/@href').get()
            chapter_name = book_chapter.xpath('.//a/span/text()').get()
            # print(chapter_name, chapter_url)
            response.meta['chapter_name'] = chapter_name
            yield Request(chapter_url, callback=self.parse_chapter,
                          headers={'Host': 'www.quanben.io', 'Referer': chapter_url}, meta=copy.copy(response.meta))

    def parse_chapter(self, response):

        chapter_url = response.url
        book_name_pinyin = "".join(chapter_url.split('/')[-2:-1])
        chapter_id = "".join(chapter_url.split('/')[-1:]).replace(".html", "")
        page = response.selector
        chapter_content = "\n".join(page.xpath('.//div[@id="content"]/p/text()').getall())
        # print('content',chapter_content)
        response.meta["book_name_pinyin"] = book_name_pinyin
        response.meta["chapter_id"] = chapter_id
        response.meta["chapter_content"] = chapter_content
        response.meta["chapter_url"] = chapter_url
        list_more_code = re.findall(self.pattern_more_url, response.text)
        if len(list_more_code) > 0:
            more_code = list_more_code[0]
            content_more_url = "%s/index.php?c=book&a=read.jsonp&callback=%s&pinyin=%s&id=%s" % (self.base_url,
                                                                                                 more_code,
                                                                                                 book_name_pinyin,
                                                                                                 chapter_id)
            yield Request(content_more_url, callback=self.parse_more_content,
                          headers={'Host': 'www.quanben.io', 'Referer': chapter_url},
                          meta=copy.copy(response.meta))
        else:
            novel_item = NovelItem()
            novel_item['book_type'] = response.meta["type_name"]
            novel_item['book_name'] = response.meta["book_name"]
            novel_item['book_url'] = response.meta["book_url"]
            novel_item['book_thumb'] = response.meta["book_thumb"]
            novel_item['book_name_pinyin'] = response.meta["book_name_pinyin"]
            novel_item['book_author'] = response.meta["book_author"]
            novel_item['book_desc'] = response.meta["book_desc"]
            novel_item['chapter_name'] = response.meta["chapter_name"]
            novel_item['chapter_id'] = response.meta["chapter_id"]
            novel_item['chapter_url'] = response.meta["chapter_url"]
            novel_item['chapter_content'] = chapter_content
            print(response.meta["book_name"], response.meta["chapter_name"], response.meta["chapter_url"])
            yield novel_item

    def parse_more_content(self, response):
        chapter_content = response.meta["chapter_content"]
        more_content = re.findall(self.pattern_more_content_json, response.text)[0]
        if more_content is not None:
            more_content = more_content.replace("<p>", "\n").replace("<\/p>", "")
            novel_item = NovelItem()
            novel_item['book_type'] = response.meta["type_name"]
            novel_item['book_name'] = response.meta["book_name"]
            novel_item['book_url'] = response.meta["book_url"]
            novel_item['book_thumb'] = response.meta["book_thumb"]
            novel_item['book_name_pinyin'] = response.meta["book_name_pinyin"]
            novel_item['book_author'] = response.meta["book_author"]
            novel_item['book_desc'] = response.meta["book_desc"]
            novel_item['chapter_name'] = response.meta["chapter_name"]
            novel_item['chapter_id'] = response.meta["chapter_id"]
            novel_item['chapter_url'] = response.meta["chapter_url"]
            novel_item['chapter_content'] = chapter_content + (
                bytes(more_content, encoding='utf8').decode('unicode_escape'))
            print(response.meta["book_name"], response.meta["chapter_name"], response.meta["chapter_url"])
            yield novel_item
