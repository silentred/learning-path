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

    ajaxBaseUrl = 'http://v.2345.com/moviecore/server/variety/index.php?'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://v.2345.com/zongyi/l/', callback=self.list_page)

    @config(age=10 * 24 * 60 * 60)
    def list_page(self, response):
        for each in response.doc('#picCon li').items():
            img = pq(each).find('div.pic>img')
            img_url = img.attr.src
            if re.match(".*noimg.jpg.*", img_url):
                img_url = img.attr.loadsrc
            rating =  pq(each).find('.sScore em').text() or 0
            save = {"small_image": img_url, "rating": rating}
            self.crawl(pq(each).find('div.txt .sTit>a').attr.href, callback=self.detail_page, save=save)

        for each in response.doc('DIV#pageList>A').items():
            if re.match("http://v.2345.com/zongyi/lpxdefault/\d+/$", each.attr.href):
                self.crawl(each.attr.href, callback=self.list_page)
            


    @config(priority=2, age=4 * 24 * 60 * 60)
    def detail_page(self, response):
        ##抓取基本信息
        categories = platform = location = orig_id = hosts= None
        catList = []
        hostList = []
        for each in response.doc('dl.dlTxt dd em.emTit'):
            # TODO 这里可以包装为一个方法，目前太乱
            if pq(each).text() == u'类型：':
                for cat in pq(each).siblings('a'):
                    catList.append(pq(cat).text())

            elif pq(each).text() == u'播出平台：':
                platform =  pq(each).siblings().eq(0).text() or None

            elif pq(each).text() == u'国家/地区：':
                location =  pq(each).siblings().eq(0).text() or None

            elif pq(each).text() == u'主持人/嘉宾：':
                for cat in pq(each).siblings('a'):
                    hostList.append(pq(cat).text())

        #get original id
        orig_id = getId(response.url, '.*zongyi/zy_(\d+)/$')

        #抓取播放源地址
        baseUrl = 'http://v.2345.com/moviecore/server/variety/index.php?'
        apis = []
        firstApi = response.doc('#playNumTabFirst').attr.apiname
        apis.append(firstApi)
        for each in response.doc('.sourceMoreList a').items():
            apis.append(each.attr.apiname)

        for apiname in apis:
            save = {"api": apiname, "variety_id": orig_id}
            self.crawl(self.ajaxBaseUrl+makeAjaxParam(api=apiname, id=orig_id), callback=self.jsonYearList, save=save)


        return {
            "url": response.url,
            "meta_title": response.doc('title').text(),
            "title": response.doc('h1 a').text() or '',
            "introduction": response.doc('#pIntroId').text() or '',
            "poster_image": response.doc('.posterCon .pic>img').attr.src or '',
            "categories": catList,
            "platform": platform or '',
            "location": location or '',
            "hosts" : hostList,
            "small_image": response.save['small_image'] or '',
            "orig_id" : orig_id,
            "rating": response.save['rating'],
            "is_play_source": 0
        }

    @config(priority=2)
    def jsonYearList(self, response):
        save = response.save
        yearList = response.json['yearList']
        #convert string yearLIst to list
        yearList = yearList[1:-1].split(',')
        for each in yearList:
            save['year'] = each
            self.crawl(self.ajaxBaseUrl+makeAjaxParam(api=save['api'], id=save['variety_id'], year=save['year']), callback=self.source_list_page, save=save)

    @config(priority=2)
    def source_list_page(self, response):
        save = response.save
        save['source'] = []
        save['is_play_source'] = 1
        for each in pq(response.json['html']).find('ul.ulPic li').items():
            img = pq(each).find('.pic img')
            guests = None
            guests = [pq(x).text() for x in pq(each).find('.sDes').children()]
            episode = {
                "img": img.attr.src or '',
                "desc": img.attr.alt or '',
                "date": pq(each).find('.pic .sExplanation em').text()[1:-1] or '',
                "guests": guests or '',
                "url": delUrlParams(pq(each).find('.aPlayBtn').attr.href)
            }
            save['source'].append(episode)
        return save


#删除url中的参数部分，返回无参的url
def delUrlParams(url):
    parsed = urlparse(url)
    empty = '', '', ''
    return urlunparse(parsed[:3] + empty) 

def getId(url, pattern=None):
    parsed = urlparse(url)
    matchObj = re.search(pattern, parsed.path)
    id = 0
    if matchObj:
        id = matchObj.group(1)
    return id

def makeAjaxParam(**params):
    defaultParam = {
        "ctl": "newDetail",
        "act": "ajaxList",
        "year": '0',
        "month": '0'
    }
    for key, value in params.items():
        defaultParam[key] = value
    pairs = [key+'='+str(value) for key,value in defaultParam.items()]
    return '&'.join(pairs)