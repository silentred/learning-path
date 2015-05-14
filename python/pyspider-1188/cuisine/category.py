#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-05-11 16:24:54
# Project: category

from pyspider.libs.base_handler import *
from pyquery import PyQuery as pq

class Handler(BaseHandler):
    crawl_config = {
        "headers" : {
            "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://home.meishichina.com/recipe-type.html', callback=self.index_page)

    @config(age=24 * 60  * 3) #minutes
    def index_page(self, response):
        #抓取一级目录和二级目录, 
        result = []
        for each in response.doc('.category_title').items():
            cat_type = each.text()
            next_wrap = each.nextAll().eq(0)
            for link in pq(next_wrap).find('a[target="_blank"]').items():
                cat = {
                    "name" : link.text(),
                    "cat_type": cat_type
                }
                result.append(cat)
        return result


    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
        #
