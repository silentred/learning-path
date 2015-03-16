#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-11 01:00:18
# Project: cat

from pyspider.libs.base_handler import *
import re
from pyquery import PyQuery as pq
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit

VTYPE = {
    'movie' : 1,
    'comic' : 2,
    'tv' : 3,
    'variety' : 4
}

class Handler(BaseHandler):
    crawl_config = {
        "headers" : {
            "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://dianying.2345.com/list/', callback=self.movie_page)


    @config(age=10 * 24 * 60 * 60)
    def movie_page(self, response):
        movie_cat = []
        for each in response.doc('.selectKeywordsList dd p').eq(0).children('a').items():
            url_rewrite = None
            match = re.search('.*list/(\w+)-+\.html$', pq(each).attr.href)
            url_rewrite = match.group(1)
            is_hot = 0
            if pq(each).attr.style is not None:
                is_hot = 1
            cat = {
                "name" : pq(each).text() or '',
                "video_type_id" : 1,
                "url_rewrite" : url_rewrite or '',
                "is_hot": is_hot
            }
            movie_cat.append(cat)

        self.crawl('http://dongman.2345.com/lt', callback=self.comic_page, save=movie_cat)

    def comic_page(self, response):
        movie_cat = response.save
        for each in response.doc('.selectKeywordsList dd p').eq(0).children('a').items():
            url_rewrite = None
            match = re.search('.*com/(\w+)/$', pq(each).attr.href)
            url_rewrite = match.group(1)
            is_hot = 0
            if pq(each).attr.style is not None:
                is_hot = 1
            cat = {
                "name" : pq(each).text() or '',
                "video_type_id" : 2,
                "url_rewrite" : url_rewrite or '',
                "is_hot": is_hot
            }
            movie_cat.append(cat)
        self.crawl('http://tv.2345.com/---.html', callback=self.tv_page, save=movie_cat)

    def tv_page(self, response):
        movie_cat = response.save
        for each in response.doc('.selectKeywordsList dd p').eq(0).children('a').items():
            url_rewrite = None
            match = re.search('.*com/(\w+)-+\.html$', pq(each).attr.href)
            url_rewrite = match.group(1)
            is_hot = 0
            if pq(each).attr.style is not None:
                is_hot = 1
            cat = {
                "name" : pq(each).text() or '',
                "video_type_id" : 3,
                "url_rewrite" : url_rewrite or '',
                "is_hot": is_hot
            }
            movie_cat.append(cat)
        self.crawl('http://v.2345.com/zongyi/l/', callback=self.variety_page, save=movie_cat)

    def variety_page(self, response):
        movie_cat = response.save
        for each in response.doc('.selectKeywordsList dd p').eq(0).children('a').items():
            url_rewrite = None
            match = re.search('.*zongyi/(\w+)/$', pq(each).attr.href)
            url_rewrite = match.group(1)
            is_hot = 0
            if pq(each).attr.style is not None:
                is_hot = 1
            cat = {
                "name" : pq(each).text() or '',
                "video_type_id" : 4,
                "url_rewrite" : url_rewrite or '',
                "is_hot": is_hot
            }
            movie_cat.append(cat)
        return movie_cat
