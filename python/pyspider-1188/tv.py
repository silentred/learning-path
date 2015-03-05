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
        self.crawl('http://tv.2345.com/---.html', callback=self.list_page)



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
            if re.match("http://tv.2345.com/----default-\d+\.html$", each.attr.href):
                self.crawl(each.attr.href, callback=self.list_page)
            


    @config(priority=2, age=4 * 24 * 60 * 60)
    def detail_page(self, response):
        ##抓取基本信息
        casting = director = categories = year = location = upd_desc = None
        for each in response.doc('dl.dlTxt dd em.emTit'):
            # TODO 这里可以包装为一个方法，目前太乱
            if pq(each).text() == u'主演：':
                castingList = []
                for cast in pq(each).siblings('a'):
                    if pq(cast).text() != u'全部主演>':
                        castingList.append(pq(cast).text())
                casting = ", ".join(castingList)

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

            elif pq(each).text() == u'国家/地区：':
                location =  pq(each).siblings().eq(0).text()

        if year is None:
            matchObj = re.search(u'.*上映于(\d+)年.*' ,response.doc('meta[name=Description]').eq(0).attr.content)
            year = matchObj.group(1)

        #抓取播放源地址
        playSources = {}
        for each in response.doc('.sourceList').items():
            api = each.attr.id[:-4]
            episodes = {}
            for episode in pq(each).find('.numList>a').items():
                if episode.attr.href and episode.attr.href[:10] != 'javascript' and pq(episode).text() != u'分集剧情':
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
        if re.match(u'.*更新.*', wrap.html()) or sep:
            pass
            if sep:
                upd_desc = wrap.contents()[-1][2:]
        else:
            closed = 1

        #测试是否能够同时去爬，并返回另一个结果
        self.crawl(response.doc('.pNumTab>a:last-child').attr.href, callback=self.plot_list_page)

        return {
            "url": response.url,
            "meta_title": response.doc('title').text(),
            "title": response.doc('h1 a').text(),
            "rating": response.doc('.sScore em').text(),
            "introduction": response.doc('#pIntroId').text()[:-9],
            "poster_image": response.doc('.posterCon .pic>img').attr.src,
            "categories": categories,
            "year": year,
            "location": location,
            "play_source": playSources,
            "small_image": response.save['small_image'],
            "casting" : casting,
            "director" : director,
            "closed": closed,
            "upd_desc": upd_desc,
            "is_plot": 0
        }

    #剧情列表
    @config(priority=2, age=4 * 24 * 60 * 60)
    def plot_list_page(self, response):
        for each in response.doc('.dramaChoice a').items():
            self.crawl(each.attr.href, callback=self.plot_detail_page)
        return self.crawl_plot_detail(response)

    @config(age=4 * 24 * 60 * 60)
    def plot_detail_page(self, response):
        return self.crawl_plot_detail(response)

    #剧情页的首页不能抓两次，以为taskId重复，所以在进入plot_list_page方法时候就要返回一次数据
    def crawl_plot_detail(self, response):
        rawHtml = response.doc('.paragraphCon').html()
        match = re.search('.*/juqing/(\d+)(-\d+)?\.html$', response.url)
        tv_id = match.group(1);
        episode_num = match.group(2)
        if episode_num is None:
            episode_num = 1
        else:
            episode_num = episode_num[1:]
        return {
            "is_plot" : 1,
            "content" : stripHtmlTag(rawHtml, 'a'),
            "tv_id": tv_id,
            "episode_num" : episode_num,
            "url": response.url
        }



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

def stripHtmlTag(string, tagName):
    return re.sub('</?'+tagName+'[^<]*>', '', string)