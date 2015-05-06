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
        self.crawl('http://dongman.2345.com/lt', callback=self.list_page)
        self.crawl('http://dongman.2345.com/', callback=self.index_page)


    @config(age=48* 60*60)
    def list_page(self, response):
        for each in response.doc('#picCon li').items():
            img = pq(each).find('div.pic>img')
            img_url = img.attr.src
            if re.match(".*noimg.jpg.*", img_url):
                img_url = img.attr.loadsrc
            small_image = {"small_image": img_url}
            self.crawl(pq(each).find('div.txt .sTit>a').attr.href, callback=self.detail_page, save=small_image)

        for each in response.doc('DIV#pageList>A').items():
            if re.match("http://dongman.2345.com/lt/\d+$", each.attr.href):
                self.crawl(each.attr.href, callback=self.list_page)

    @config(age=12* 60*60, priority=10)
    def index_page(self, response):
        for each in response.doc('.ul_picTxtA li').items():
            img = pq(each).find('div.pic>img')
            img_url = img.attr.src
            if re.match(".*noimg.jpg.*", img_url):
                img_url = img.attr.loadsrc
            small_image = {"small_image": img_url}
            self.crawl(pq(each).find('.playBtn>a').attr.href, callback=self.detail_page, save=small_image)
    
    @config(priority=4, age=18* 60*60)
    def on_message(self, project, msg):
        self.crawl(msg['url'], callback=self.detail_page )


    def handleMetaRedirect(self, response):
        meta = response.doc('meta[http-equiv=refresh]')
        url = None
        if meta is not None and meta.attr.content is not None:
            match = re.search("URL='(.*)'", meta.attr.content or '')
            if match is not None:
                url = match.group(1)
        if url is not None:
            self.crawl(url, callback=self.detail_page, save=response.save)

    @config(priority=2, age=18* 60*60)
    def detail_page(self, response):
        self.handleMetaRedirect(response)
        ##抓取基本信息
        categories = year = location = alias = upd_desc = orig_id = None
        catList = []
        for each in response.doc('dl.dlTxt dd em.emTit'):
            # TODO 这里可以包装为一个方法，目前太乱
            if pq(each).text() == u'类型：':
                for cat in pq(each).siblings('a'):
                    catList.append(pq(cat).text())

            elif pq(each).text() == u'年代：':
                year =  pq(each).siblings().eq(0).text() or None

            elif pq(each).text() == u'国家/地区：':
                location =  pq(each).siblings().eq(0).text() or None

            elif pq(each).text() == u'别名：':
                alias =  pq(each).siblings().eq(0).text() or None

        #抓取播放源地址
        playSources = {}
        for each in response.doc('.sourceList').items():
            if each.attr.id is not None and len(each.attr.id)>4:
                api = each.attr.id[:-4]
                episodes = {}
                for episode in pq(each).find('.numList>a').items():
                    if episode.attr.href and episode.attr.href[:10] != 'javascript':
                        episodes[pq(episode).text()] = delUrlParams(episode.attr.href)
                playSources[api] = episodes
        #这里必须处理一种情况：sohu_con 和sohu_con_list其实是一种播放源，
        #因为集数太多，所以分了两个列表，需要合并两个dict
        for key in playSources.keys():
            if playSources.has_key(key+'_con_'):
                playSources[key] = dict(playSources[key].items() + playSources[key+'_con_'].items())
                del playSources[key+'_con_']


        #判断是否完结，closed:0 | 1 
        closed = 0
        wrap = response.doc('.pTxt .sDes')
        sep = wrap.find('i')
        if re.match(u'.*更新.*', wrap.text()) or sep:
            pass
            if sep:
                upd_desc = wrap.contents()[-1][2:] or None
        else:
            closed = 1

        #get original id
        orig_id = getId(response.url, '.*dm/(\d+)\.html$')

        small_image = response.save['small_image']
        if small_image is None or len(small_image)==0:
            small_image = poster_image

        return {
            "url": response.url,
            "meta_title": response.doc('title').text(),
            "title": response.doc('h1 a').text() or '',
            "rating": response.doc('.sScore em').text() or '',
            "introduction": response.doc('#pIntroId').text() or '',
            "poster_image": response.doc('.posterCon .pic>img').attr.src or '',
            "categories": catList,
            "year": year or '',
            "location": location or '',
            "alias" : alias or '',
            "play_source": playSources,
            "closed": closed,
            "upd_desc" : upd_desc or '',
            "small_image": small_image or '',
            "orig_id" : orig_id
        }
