# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''

CREATE TABLE chapters_table_1 (
id INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
book_name VARCHAR(255),
book_name_pinyin VARCHAR(255),
book_desc TEXT, 
book_url VARCHAR(255), 
book_thumb VARCHAR(255), 
book_type VARCHAR(255), 
book_author VARCHAR(255), 
chapter_name VARCHAR(255), 
chapter_id INT, 
chapter_url VARCHAR(255), 
chapter_content MEDIUMTEXT
)ENGINE=INNODB DEFAULT CHARSET=utf8;
'''


class NovelItem(scrapy.Item):
    # define the fields for your item here like:
    book_name = scrapy.Field()
    book_name_pinyin = scrapy.Field()
    book_desc = scrapy.Field()
    book_url = scrapy.Field()
    book_thumb = scrapy.Field()
    book_type = scrapy.Field()
    book_author = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_id = scrapy.Field()
    chapter_url = scrapy.Field()
    chapter_content = scrapy.Field()
