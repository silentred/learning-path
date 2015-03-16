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
        self.crawl('http://dianying.2345.com/list/', callback=self.list_page)


    @config(age=10 * 24 * 60 * 60)
    def list_page(self, response):
        for each in response.doc('#picCon li').items():
            img = pq(each).find('div.pic>img')
            img_url = img.attr.src
            if re.match(".*noimg.jpg.*", img_url):
                img_url = img.attr.loadsrc
            small_image = {"small_image": img_url}
            self.crawl(pq(each).find('div.txt .sTit>a').attr.href, callback=self.detail_page, save=small_image)

        for each in response.doc('DIV#pageList>A').items():
            if re.match("http://dianying.2345.com/list/-------\d+\.html$", each.attr.href):
                self.crawl(each.attr.href, callback=self.list_page)
            


    @config(priority=2, age=1 * 24 * 60 * 60)
    def detail_page(self, response):
        ##抓取基本信息
        casting= director= categories= specialties= runtime= year= location= poster_image = lang = play_source = title = None
        castingList = []
        catList = []
        sepList = []
        for each in response.doc('dl.dlTxt dd em.emTit'):
            # TODO 这里可以包装为一个方法，目前太乱
            if pq(each).text() == u'主演：':
                for cast in pq(each).siblings('a'):
                    castingList.append(pq(cast).text())

            elif pq(each).text() == u'导演：':
                director = pq(each).siblings().eq(0).text() or ''

            elif pq(each).text() == u'类型：':
                for cat in pq(each).siblings('a'):
                    catList.append(pq(cat).text())

            elif pq(each).text() == u'看点：':
                for cat in pq(each).siblings('a'):
                    sepList.append(pq(cat).text())

            elif pq(each).text() == u'时长：':
                runtime =  pq(each).siblings().eq(0).text() or ''

            elif pq(each).text() == u'年代：':
                year =  pq(each).siblings().eq(0).text() or ''

            elif pq(each).text() == u'国家/地区：':
                location =  pq(each).siblings().eq(0).text() or ''

            elif pq(each).text() == u'语言：':
                lang =  pq(each).siblings().eq(0).text() or ''

        #抓取播放源地址
        playSources = {}
        for each in response.doc('.sourceTab>a'):
            playSources[pq(each).attr.data[:-2]] = delUrlParams(pq(each).attr.href)

        #还存在一种旧的的模板，需要对没有抓到的内容再次抓取
        poster_image = response.doc('.posterCon .pic>img').attr.src or response.doc('.detailPicIntro img').attr.src
        title = response.doc('h1 a').text() or response.doc('.titleName .sName').text()
        introduction = response.doc('#pIntroId').text() or response.doc('#intro').text()
        for each in response.doc('.txt .sTit'):
            if len(catList) < 1:
                if pq(each).text() == u'类型：':
                    catList = pq(each).siblings('span').text().split(' ')
            if location is None:
                if pq(each).text() == u'地区：':
                    location = pq(each).siblings('span').text() or ''
            if year is None:
                if pq(each).text() == u'年代：':
                    year = pq(each).parents('p').contents()[1] or ''
        for each in response.doc('.col_b>div>div>dl>dt'):
            if len(castingList) < 1:
                if pq(each).text() == u'主演：':
                    castingList = [pq(actor).text() for actor in pq(pq(each).nextAll('dd')[0]).find('a') ]
            if director is None:
                if pq(each).text() == u'导演：':
                    director = pq(pq(each).nextAll('dd')[0]).find('a').text() or ''

        if len(playSources) < 1:
            for each in response.doc('.moviePlaySourceA p a').items():
                playSources[pq(each).attr.apiname] = delUrlParams(pq(each).attr.href)

        mainResult = {
            "url": response.url,
            "meta_title": response.doc('title').text(),
            "title": title or '',
            "rating": response.doc('.sScore em').eq(0).text() or '',
            "casting": castingList,
            "introduction": introduction or '',
            "play_source": playSources,
            "poster_image": poster_image or '',
            "director": director or '',
            "categories": catList,
            "specialties": sepList,
            "runtime": runtime or '',
            "year": year or '',
            "location": location or '',
            "lang" : lang or '',
            "small_image" : response.save['small_image'] or '',
            "orig_id": getId(response.url, '(\d+).html$') or ''
        }

        return mainResult

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