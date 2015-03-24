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

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://dianying.2345.com/', callback=self.movie_index)
        self.crawl('http://dongman.2345.com/', callback=self.comic_index)
        self.crawl('http://tv.2345.com/', callback=self.tv_index)
        self.crawl('http://v.2345.com/zongyi/', callback=self.variety_index)
        self.crawl('http://v.2345.com/', callback=self.index_index)

    def index_index(self, response):
        items = []
        for each in response.doc('.mod_a').items():
            section = pq(each).find('span.sMark').eq(0).text()
            video_type_id = getVideoTypeIdByName(section)
            for item in pq(each).find('.pTabList a').items():
                sub_section = pq(item).text()
                length = len(pq(item).attr.name)
                content_id = pq(item).attr.id[:length]+ '_content' + pq(item).attr.id[length:]
                for x in pq(each).find("#"+content_id+" ul li").items():
                    cover = pq(x).find('.pic img').attr.loadsrc
                    url = pq(x).find('.playBtn a').attr.href
                    desc = pq(x).find('.sDes').text()
                    orig_id = getOrigId(url)
                    items.append({
                        "page_id": 0,
                        "section": sub_section,
                        "cover": cover,
                        "url" : url, 
                        "desc": desc,
                        "orig_id": orig_id,
                        "video_type_id": video_type_id
                        })
        #banner
        for each in response.doc('#focus ul li').items():
            cover = pq(each).find("img").attr.loadsrc or pq(each).find("img").attr.src
            url = pq(each).find('.playBtn a').attr.href
            orig_id = getOrigId(url)
            video_type_id = detectVideoType(pq(each).find('i.videoStyleLogo'))
            if orig_id is not None:
                items.append({
                            "page_id": 0,
                            "section": "banner",
                            "cover": cover,
                            "url" : url, 
                            "desc": '',
                            "orig_id": orig_id,
                            "video_type_id": video_type_id
                    })
            
        return items



    @config(age=10 * 24 * 60 * 60)
    def movie_index(self, response):
        movieIndexItems = []
        for each in response.doc('.mod_e').items():
            section = pq(each).find('span.sMark').text()
            for item in pq(each).find('ul.ul_picTxtA >li').items():
                cover = pq(item).find('.pic img').attr.loadsrc
                url = delUrlParams(pq(item).find('.playBtn a').attr.href)
                orig_id = re.search('.*/detail/(\d+)\.html',url).group(1)
                desc = pq(item).find('.sDes').text()
                movieIndexItems.append({
                    "section": section,
                    "cover": cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "video_type_id": 1,
                    "page_id": 1
                    })
                
        #banner
        for each in response.doc('#topBannerFocus_Con ul li').items():
            orig_id = None
            cover = pq(each).find('img').attr.src
            url = delUrlParams(pq(each).find('a').attr.href)
            matchObj = re.search('.*/detail/(\d+)\.html',url)
            if matchObj is not None:
                orig_id = matchObj.group(1)
            desc = pq(each).find('.sDes').text()
            if orig_id is not None:
                movieIndexItems.append({
                    "section": 'banner',
                    "cover": cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "video_type_id": 1,
                    "page_id": 1
                })

        for x in movieIndexItems:
            self.send_message('movie', {"url": x['url']})

        return movieIndexItems

    @config(age=10 * 24 * 60 * 60)
    def comic_index(self, response):
        items = []
        for each in response.doc('.mod_g').items():
            section = pq(each).find('.animationPng a').text()
            for item in pq(each).find('.ul_picTxtA li').items():
                cover = pq(item).find('.pic img').attr.loadsrc
                url = delUrlParams(pq(item).find('.playBtn a').attr.href)
                orig_id = re.search('.*/dm/(\d+)\.html',url).group(1)
                desc = pq(item).find('.sDes').text()
                items.append({
                    "section": section,
                    "cover": cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "video_type_id": 2,
                    "page_id": 2
                    })
        #banner
        for each in response.doc('#focus ul li').items():
            cover = pq(each).find('img').attr.loadsrc
            url = delUrlParams(pq(each).find('.sName a').attr.href)
            desc = pq(each).find('.sTxt').text()
            orig_id = None
            matchObj = re.search('.*/dm/(\d+)\.html',url)
            if matchObj is not None:
                orig_id = matchObj.group(1)
            
            if orig_id is not None:
                items.append({
                "section": 'banner',
                "cover": cover,
                "url": url,
                "orig_id": orig_id,
                "desc": desc,
                "video_type_id": 2,
                "page_id": 2
                })
            
        # 另外一种板式
        for each in response.doc('.mod_h .th_h'):
            section = pq(each).find('.mark').text() or pq(each).find('.sTit').text()
            nextNode = pq(each).nextAll('.tb_h').eq(0)
            for item in pq(nextNode).find('.ul_picTxtA li').items():
                cover = pq(item).find('img').attr.loadsrc
                url = delUrlParams(pq(item).find('.sName a').attr.href)
                desc = pq(each).find('.sTxt').text() or pq(each).find('.sDes').text() 
                orig_id = re.search('.*/dm/(\d+)\.html',url).group(1)
                items.append({
                    "section": section,
                    "cover": cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "video_type_id": 2,
                    "page_id": 1
                    })

        for x in items:
            self.send_message('comic', {"url": x['url']})

        return items
        
    @config(age=10 * 24 * 60 * 60)
    def tv_index(self, response):
        items = []
        for each in response.doc('.mod_a').items():
            section = pq(each).find('.th_a .sMark').text()
            for item in pq(each).find('.tb_a .picTxt li').items():
                cover = pq(item).find('.pic img').attr.loadsrc
                url = delUrlParams(pq(item).find('.playBtn').attr.href)
                orig_id = re.search('.*/detail/(\d+)\.html',url).group(1)
                desc = pq(item).find('.sDes').text()
                items.append({
                    "section": section,
                    "cover": cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "video_type_id": 3,
                    "page_id": 3
                    })

        #banner
        for each in response.doc('#topBannerFocus_Con ul li').items():
            cover = pq(each).find('img').attr.src
            url = delUrlParams(pq(each).find('a').attr.href)
            desc = pq(each).find('.sDes').text()
            orig_id = None
            matchObj = re.search('.*/detail/(\d+)\.html',url)
            if matchObj is not None:
                orig_id = matchObj.group(1)
            if orig_id is not None:
                items.append({
                    "section": 'banner',
                    "cover": cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "video_type_id": 3,
                    "page_id": 3
                })

        for x in items:
            self.send_message('tv', {"url": x['url']})
        return items


    @config(age=10 * 24 * 60 * 60)
    def variety_index(self, response):
        items = []
        for each in response.doc('.mod_c .th_c'):
            section = pq(each).find('.sMark').text()
            content = pq(each).nextAll('.tb_c').eq(0)
            for item in pq(content).find('.ul_picTxtD li').items():
                cover = pq(item).find('.pic img').attr.loadsrc
                url = delUrlParams(pq(item).find('.playBtn a').attr.href)
                orig_id = re.search('.*/zongyi/zy_(\d+)',url).group(1)
                desc = pq(item).find('.sDes').text()
                items.append({
                    "section": section,
                    "cover": cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "video_type_id": 4,
                    "page_id": 4
                }) 
        #banner
        i = 0
        for each in response.doc('#focus .picCon .con').items():
            url = pq(each).find('a').attr.href
            big_cover = pq(each).find('img').attr.loadsrc
            orig_id = re.search('.*/zongyi/zy_(\d+)',url).group(1)
            desc =  pq(item).find('.pTxt').text()
            cover = response.doc("#pic_%d img" % i ).attr.src
            i +=1
            items.append({
                 "section": "banner",
                    "cover": cover,
                    "big_cover": big_cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "video_type_id": 4,
                    "page_id": 4
                })

        #hot
        hot =  response.doc('.mod_e').eq(0)
        section = pq(hot).find('span.sMark').text()
        firstHot = pq(hot).find('.firstHot')
        big_cover = pq(firstHot).find('.pic img').attr.src
        desc = pq(firstHot).find('.pic .sDes').text()
        broadcast_time = pq(firstHot).find('.pic .sTimeBg').text()
        url = pq(firstHot).find('.playBtn a').attr.href
        orig_id = re.search('.*/zongyi/zy_(\d+)',url).group(1)
        long_desc = pq(firstHot).find('.txt p').text()
        items.append({
                    "section": section,
                    "big_cover": big_cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "broadcast_time": broadcast_time,
                    "long_desc": long_desc,
                    "video_type_id": 4,
                    "page_id": 4
            })
        for each in pq(hot).find('.ul_picTxtD li').items():
            url = pq(each).find('.sName a').attr.href
            cover = pq(each).find('.pic img').attr.src
            orig_id = re.search('.*/zongyi/zy_(\d+)',url).group(1)
            desc =  pq(each).find('.sDes').text()
            items.append({
                    "section": section,
                    "cover": cover,
                    "url": url,
                    "orig_id": orig_id,
                    "desc": desc,
                    "video_type_id": 4,
                    "page_id": 4
                })
        
        for x in items:
            self.send_message('variety', {"url": x['url']})

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