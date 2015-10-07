#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-05-12 13:34:11
# Project: meishi_material

from pyspider.libs.base_handler import *
from pyquery import PyQuery as pq
import re, json

class Handler(BaseHandler):
    crawl_config = {
        "headers" : {
            "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"
        }
    }

    headers = {
        "Accept-Language": "zh-CN",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip,deflate",
        "X-Requested-With": "XMLHttpRequest",
        "Host": 'dianying.fm',
        "User-Agent": 'Mozilla/5.0 (Windows NT 5.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
    }

    cookies = {
        "after_login_url":'/profile/',
        "csrftoken": '9SY570rByO7ec8qjxHwCTKdSrCn5rohc',
        "sessionid":'.eJxVyzsOwjAMBuC7eEZVnBAV2MrExNIDRHZsFARqpSaZUO_egBhg_B_fCwLVkkLNuoREOcEJIjtPLD2rt8Ywigr7w42coBzVyt61iCSw-8VM8aGTNE8xznUq3WfLibC7ziM9y3gZcGjd-fv84_e3RN9bg7Bu4AUyBA:1ZjU33:EqLX-8XklI3u-LNFD1a1EXoRe9c'
    }

    @every(minutes=24*60)
    def on_start(self):
        self.crawl('http://dianying.fm/search/', callback=self.index_page)


    @config(age=24*60 * 3)
    def list_page(self, response):
        for each in response.doc('.fm-result-list .fm-movie-title a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

        for list_link in response.doc('#pagination a').items():
            list_href = pq(list_link).attr.href
            if list_href is not None and len(list_href)>0 :
                self.crawl(list_href, callback=self.list_page)

    @config(age=24*60)
    def index_page(self, response):
        for each in response.doc('.fm-category-tags a').items():
            self.crawl(each.attr.href, callback=self.list_page)

    @config(priority=2)
    def detail_page(self, response):
        full_name = response.doc('.fm-title h3 a').text()
        year = response.doc('.fm-title .fm-genres .fm-genre:first-child').text()
        style = response.doc('.fm-title .fm-genres .fm-genre:nth-child(2)').text()
        intro = response.doc('.fm-summary').text()
        poster_src = response.doc('.fm-intro img').attr.src

        db_rate_dom = response.doc('.fm-title .fm-rating .fm-green')
        db_rate = db_rate_dom.text()
        db_link = db_rate_dom.attr.href

        im_rate_dom = response.doc('.fm-title .fm-rating .fm-orange')
        im_rate = im_rate_dom.text()
        im_link = im_rate_dom.attr.href

        infos = response.doc('.fm-minfo dd')
        director = pq(infos.eq(0)).text()
        starings = []
        for x in pq(infos.eq(1)).find('a').items():
            starings.append(x.text())
        area = pq(infos.eq(2)).text()
        first_date = pq(infos.eq(3)).text()
        span = pq(infos.eq(4)).text()
        alias = pq(infos.eq(5)).text()

        albums = []
        for x in response.doc('.fm-little ul li a').items():
            albums.append(x.text())

        pics = []
        for x in response.doc('.fm-psmm a').items():
            pics.append(x.attr['data-hover-img'])

        movie = {
            "name": full_name,
            "intro":  intro,
            "year": year, 
            "style" : style,
            "db_link": db_link,
            "db_rate": db_rate,
            "im_link": im_link,
            "im_rate": im_rate,
            "url": response.url,
            "director": director,
            "starings": starings,
            "area": area,
            "first_date": first_date,
            "span": span,
            "alias": alias,
            "albums": albums,
            "pics": pics
        }

        megnet_url = response.url + 'playlinks/magnet'
        self.headers['Referer'] = response.url
        self.crawl(megnet_url, callback=self.link_page, headers=self.headers, cookies=self.cookies, save={"movie": movie})


    @config(priority=2)
    def link_page(self, response):
        megnets = []
        if response.ok and response.json['count'] > 0:
            html = response.json["html"]
            for x in pq(html).find('tr').items():
                source = x.find('td').eq(2).text()
                title = x.find('td').eq(3).text()
                url = x.find('td').eq(6).find('a').attr.href
                megnets.append({"source": source, "title": title, "url":url})

        return {
            "movie": response.save["movie"],
            "megnets": megnets
        }

def getPics(html):
    match = re.search('var J_photo = (.*);', html)
    if match is not None:
        obj_string = match.group(1)
    obj = json.JSONDecoder().decode(obj_string)
    return obj

def isRecipeUrl(url):
    return re.match('^.*/recipe-(\d+).html$', url)