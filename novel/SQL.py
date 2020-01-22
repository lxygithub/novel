#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by luoxingyuan on 2018/3/1 23:25.
# Email: mewlxy@foxmail.com

import pymysql.cursors

from novel import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB
MYSQL_CHARSET = settings.MYSQL_CHARSET

conn = pymysql.connect(user=MYSQL_USER,
                       password=MYSQL_PASSWORD,
                       host=MYSQL_HOSTS,
                       database=MYSQL_DB,
                       charset=MYSQL_CHARSET)
cursor = conn.cursor()
sql_create_table = '''
CREATE TABLE IF NOT exists chapters_table_%s (
id INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
book_name VARCHAR(255),
book_name_pinyin VARCHAR(255),
book_desc VARCHAR(255), 
book_url VARCHAR(255), 
book_thumb VARCHAR(255), 
book_type VARCHAR(255), 
book_author VARCHAR(255), 
chapter_name VARCHAR(255), 
chapter_url VARCHAR(255), 
chapter_id INT, 
chapter_content MEDIUMTEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)ENGINE=INNODB DEFAULT CHARSET=utf8;

'''


class Sql(object):
    table_rows_count = 0
    table_count = 2

    @staticmethod
    def count_rows(table_name):
        sql = 'SELECT COUNT(*) FROM %s;' % table_name
        cursor.execute(sql)
        res = cursor.fetchall()

    @staticmethod
    def create_table():
        Sql.table_count += 1
        sql = sql_create_table % str(Sql.table_count)
        cursor.execute(sql)
        conn.commit()

    @staticmethod
    def insert_chapter(item):
        sql = '''
                INSERT INTO chapters_table_%s (book_name,book_name_pinyin,book_desc,book_url,book_thumb,book_type,book_author,
                chapter_name,chapter_url,chapter_id,chapter_content)
                 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');
              '''

        sql1 = sql % (str(Sql.table_count), item["book_name"],
                      item["book_name_pinyin"],
                      item["book_desc"],
                      item["book_url"],
                      item["book_thumb"],
                      item["book_type"],
                      item["book_author"],
                      item["chapter_name"],
                      item["chapter_url"],
                      item["chapter_id"],
                      item["chapter_content"])
        cursor.execute(sql1)
        conn.commit()
        Sql.table_rows_count += 1
        if Sql.table_rows_count >= 100000:
            Sql.create_table()
            Sql.table_rows_count = 0

    # 错误处理方法
    @staticmethod
    def _handle_error(failure, item, spider):
        # cursor.close()
        print(failure)
