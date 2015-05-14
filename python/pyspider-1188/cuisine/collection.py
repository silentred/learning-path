#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-05-11 16:24:54
# Project: category

from pyspider.libs.base_handler import *
from pyquery import PyQuery as pq
import re

class Handler(BaseHandler):
    crawl_config = {
        "headers" : {
            "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://home.meishichina.com/collect-list-type-recipe.html', callback=self.list_page)

    @config(age=24 * 60) #minutes
    def list_page(self, response):
        for each in response.doc('#J_list li h4>a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

        for list_link in response.doc('.ui-page-inner a').items():
            list_href = pq(list_link).attr.href
            if list_href is not None and len(list_href)>0 :
                self.crawl(list_href, callback=self.list_page)
                

    @config(priority=2, age=24 * 60)
    def detail_page(self, response):
        name = response.doc('h1.recipe_De_title').text()
        intro = response.doc('#collect_txt1').text()
        orig_id = re.search('^.*/collect-(\d+).html$', response.url).group(1)
        return {
            "name": name,
            "intro": intro ,
            "orig_id": orig_id
        }
        
