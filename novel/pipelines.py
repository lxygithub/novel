# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from novel.SQL import Sql
from novel.items import NovelItem


class NovelPipeline(object):

    def process_item(self, item, spider):
        Sql.insert_chapter(item)
        return item
