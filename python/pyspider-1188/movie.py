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
        casting= director= categories= specialties= runtime= year= location= lang = play_source = ''
        for each in response.doc('dl.dlTxt dd em.emTit'):
            # TODO 这里可以包装为一个方法，目前太乱
            if pq(each).text() == u'主演：':
                castingList = []
                for cast in pq(each).siblings('a'):
                    castingList.append(pq(cast).text())
                casting = ", ".join(castingList[:-1])

            elif pq(each).text() == u'导演：':
                directorList = []
                for director in pq(each).siblings('a'):
                    directorList.append(pq(director).text())
                director = ", ".join(directorList)

            elif pq(each).text() == u'类型：':
                catList = []
                for cat in pq(each).siblings('a'):
                    catList.append(pq(cat).text())
                categories = ", ".join(catList)

            elif pq(each).text() == u'看点：':
                sepList = []
                for cat in pq(each).siblings('a'):
                    sepList.append(pq(cat).text())
                specialties = ", ".join(sepList)

            elif pq(each).text() == u'时长：':
                runtime =  pq(each).siblings().eq(0).text()

            elif pq(each).text() == u'年代：':
                year =  pq(each).siblings().eq(0).text()

            elif pq(each).text() == u'国家/地区：':
                location =  pq(each).siblings().eq(0).text()

            elif pq(each).text() == u'语言：':
                lang =  pq(each).siblings().eq(0).text()

        #抓取播放源地址
        playSources = []
        for each in response.doc('.sourceTab>a'):
            playSources.append(delUrlParams(pq(each).attr.href))
        play_source = ", ".join(playSources)

        mainResult = {
            "url": response.url,
            "meta_title": response.doc('title').text(),
            "title": response.doc('h1 a').text(),
            "rating": response.doc('.sScore em').text(),
            "casting": casting,
            "introduction": response.doc('#pIntroId').text()[:-9],
            "play_source": play_source,
            "poster_image": response.doc('.posterCon .pic>img').attr.src,
            "director": director,
            "categories": categories,
            "specialties": specialties,
            "runtime": runtime,
            "year": year,
            "location": location,
            "lang" : lang,
            "small_image" : response.save['small_image'],
            "orig_id": getId(response.url, '(\d+).html$')
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
    i