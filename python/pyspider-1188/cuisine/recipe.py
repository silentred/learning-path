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

    @every(minutes=24*60)
    def on_start(self):
        self.crawl('http://home.meishichina.com/recipe-list.html', callback=self.list_page)
        self.crawl('http://home.meishichina.com/recipe.html', callback=self.index_page)
        self.crawl('http://home.meishichina.com/collect-list-type-recipe.html', callback=self.collection_list)
        self.crawl('http://www.meishichina.com/YuanLiao/', callback=self.material_page)


    @config(age=24*60 * 3)
    def list_page(self, response):
        for each in response.doc('.ui_list_1 ul h4 a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

        for list_link in response.doc('.ui-page-inner a').items():
            list_href = pq(list_link).attr.href
            if list_href is not None and len(list_href)>0 :
                self.crawl(list_href, callback=self.list_page)

    @config(age=24*60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if isRecipeUrl(response.url):
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(age=24*60 * 3)
    def collection_list(self, response):
        for each in response.doc('#J_list li h4>a').items():
            self.crawl(each.attr.href, callback=self.list_page)

        for list_link in response.doc('.ui-page-inner a').items():
            list_href = pq(list_link).attr.href
            if list_href is not None and len(list_href)>0 :
                self.crawl(list_href, callback=self.collection_list)

    @config(age=24*60 * 3)
    def material_page(self, response):
        for each in response.doc('.category_sub2 a').items():
            self.crawl(each.attr.href, callback=self.list_page)

    @config(priority=2)
    def detail_page(self, response):
        name = response.doc('h1.recipe_De_title').text()
        intro = response.doc('#block_txt1').text()

        pics = []
        script = response.doc('script').text()
        raw_pics = getPics(script)
        for x in raw_pics:
            pics.append(x['src'])

        cats = []
        for x in response.doc('.recipeTag a').items():
            cats.append(x.text())

        main_material = []
        comdiment = []
        tool = ''

        for x in response.doc('.recipeCategory_sub_L').items():
            sibling = pq(x).siblings('.recipeCategory_sub_R')
            if x.text() == u'主料':
                for material in pq(sibling).find('li').items():
                    main_material.append({
                        pq(material).find('.category_s1').text():pq(material).find('.category_s2').text()
                    })
            elif x.text() == u'调料':
                for material in pq(sibling).find('li').items():
                    comdiment.append({
                        pq(material).find('.category_s1').text():pq(material).find('.category_s2').text()
                    })
            elif x.text() == u'厨具':
                tool = pq(sibling).find('li').text()
        
        procedure = []
        for x in response.doc('.recipeStep ul li').items():
            img = pq(x).find('.recipeStep_img img').attr.src
            method = pq(x).find('.recipeStep_word').text()
            index = pq(x).find('.recipeStep_word img').attr.alt
            procedure.append({
                "i":int(index),
                "img": img or '',
                "method": method or ''
            })

        tips = response.doc('.recipeTip').html()
        orig_id = re.search('^.*/recipe-(\d+).html$', response.url).group(1)
        
        return {
            "name": name,
            "intro":  intro,
            "pics": pics, 
            "cats" : cats,
            "main_material" : main_material,
            "comdiment": comdiment, 
            "tool" : tool,
            "procedure": procedure,
            "tips": tips, 
            "orig_id": orig_id
        }


def getPics(html):
    match = re.search('var J_photo = (.*);', html)
    if match is not None:
        obj_string = match.group(1)
    obj = json.JSONDecoder().decode(obj_string)
    return obj

def isRecipeUrl(url):
    return re.match('^.*/recipe-(\d+).html$', url)