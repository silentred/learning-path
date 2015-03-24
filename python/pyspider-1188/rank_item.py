#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

from pyspider.libs.base_handler import *
import re
from pyquery import PyQuery as pq
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit

class Handler(BaseHandler):
    crawl_config = {
        "headers" : {
            "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"
        }
    }

    @every(minutes=20 * 60)
    def on_start(self):
        self.crawl('http://dianying.2345.com/top/', callback=self.rank_item, save={'video_type_id':1})
        self.crawl('http://tv.2345.com/top/', callback=self.rank_item, save={'video_type_id':3})
        self.crawl('http://tv.2345.com/dongman/top/', callback=self.rank_item, save={'video_type_id':2})
        self.crawl('http://tv.2345.com/zongyi/top/', callback=self.rank_item, save={'video_type_id':4})

    @config(age=12 * 24 * 60 * 60)
    def rank_item(self, response):
        items = []
        section = response.doc('.tabList a.cur').text()
        video_type_id = response.save['video_type_id']
        for each in response.doc('.rankTable tr[name=tr_hover]').items():
            td =  pq(each).find('td').eq(0)
            url = pq(td).find('a').attr.href
            orig_id = getOrigId(url)
            position =  pq(td).find('i').text()
            items.append({
                "section": section,
                "video_type_id": video_type_id, 
                "url": url,
                "orig_id": orig_id, 
                "position": position
                })

        for each in response.doc('.tabList a').items():
            self.crawl(each.attr.href, callback=self.rank_item, save={'video_type_id': video_type_id})

        return items


            
#删除url中的参数部分，返回无参的url
def delUrlParams(url):
    parsed = urlparse(url)
    empty = '', '', ''
    return urlunparse(parsed[:3] + empty) 

#得到视频的id
def getId(url, pattern=None):
    parsed = urlparse(url)
    matchObj = re.search(pattern, parsed.path)
    id = 0
    if matchObj:
        id = matchObj.group(1)
    return id

def getOrigId(url):
    zongyi = '.*/zongyi/zy_(\d+)'
    detail = '.*/detail/(\d+)\.html'
    dm = '.*/dm/(\d+)\.html'
    if re.match(zongyi, url):
        return re.search(zongyi, url).group(1)
    elif re.match(detail,url):
        return re.search(detail, url).group(1)
    elif re.match(dm,url):
        return re.search(dm,url).group(1)

def getVideoTypeIdByName(name):
    if name == u'电视剧':
        return 3
    elif name == u'电影':
        return 1
    elif name == u'动漫':
        return 2
    elif name == u'综艺':
        return 4

def detectVideoType(node):
    if pq(node).hasClass('videoStyleLogoA'):
        return 3
    elif pq(node).hasClass('videoStyleLogoC'):
        return 4
    else:
        return 1