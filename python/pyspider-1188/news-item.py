#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

from pyspider.libs.base_handler import *
import re,  time, random, errno, os, urllib
from pyquery import PyQuery as pq
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
from projects.movie import delUrlParams, getId, mkdir_p, downlaodImage

class Handler(BaseHandler):
    crawl_config = {
        "headers" : {
            "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"
        }
    }

    @every(seconds=23* 60*60)
    def on_start(self):
        self.crawl('http://v.2345.com/', callback=self.index_page)
        self.crawl('http://v.2345.com/zongyi/', callback=self.variety_page)

    @config(age=12* 60*60)
    def index_page(self, response):
        newsList = []
        for each in response.doc('#todayHot .picTxt li').items():
            img = pq(each).find('div.pic>img')
            img_url = img.attr.src
            if re.match(".*noimg.jpg.*", img_url):
                img_url = img.attr.loadsrc
            title = pq(each).find('.pIntro .sTit').text()
            if title is None or len(title)==0:
                title = pq(each).find('.pIntro').text()
            url = pq(each).find('.aPlayBtn').attr.href
            news = {
                "url": url,
                "title": title,
                "cover": img_url,
                "page_id": 0,
                "section": 'news'
            }
            newsList.append(news);
        return newsList

    @config(age=12* 60*60)
    def variety_page(self, response):
        updateList = []
        for each in response.doc('.newUpate ul li').items():
            achor = pq(each).find('.sTit > a')
            url = achor.attr.href
            video_id = 0
            match = re.match('.*/zongyi/zy_(\d+)', url)
            if match is not None:
                url = ''
                video_id = match.group(1)
            title = achor.text()
            desc = pq(each).find('.sDes').text()
            item = {
                "url": url,
                "video_id": video_id,
                "title": title,
                "desc": desc,
                "page_id": 4,
                "section": 'new_updates'
            }
            updateList.append(item)

        for each in response.doc('.ul_TxtE li a').items():
            url = each.attr.href
            title = each.text()
            video_id = 0
            match = re.match('.*/zongyi/zy_(\d+)', url)
            if match is not None:
                url = ''
                video_id = match.group(1)
            item = {
                "url": url,
                "video_id": video_id,
                "title": title,
                "page_id": 4,
                "section": 'entertain_news'
            }
            updateList.append(item)

        return updateList

