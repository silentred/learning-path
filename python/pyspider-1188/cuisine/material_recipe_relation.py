#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-05-12 13:34:11
# Project: meishi_material

from pyspider.libs.base_handler import *
from pyquery import PyQuery as pq
import re, json
from projects.meishi_recipe import isRecipeUrl

class Handler(BaseHandler):
    crawl_config = {
        "headers" : {
            "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"
        }
    }

    @every(minutes=24*60)
    def on_start(self):
        self.crawl('http://home.meishichina.com/collect-list-type-recipe.html', callback=self.collection_list)
        self.crawl('http://www.meishichina.com/YuanLiao/', callback=self.material_page)


    @config(age=24*60 * 3)
    def list_page(self, response):
        for list_link in response.doc('.ui-page-inner a').items():
            list_href = pq(list_link).attr.href
            if list_href is not None and len(list_href)>0 :
                self.crawl(list_href, callback=self.list_page, save=response.save)

        orig_ids = []
        for list_link in response.doc('.ui_list_1 h4>a').items():
            if isRecipeUrl(list_link.attr.href):
                orig_id = re.search('^.*/recipe-(\d+).html$', list_link.attr.href).group(1)
                orig_ids.append(orig_id)
        return {
            "name": response.save['name'],
            "type_name": response.save['type_name'],
            "orig_ids": orig_ids,
        }

    @config(age=24*60 * 3)
    def collection_list(self, response):
        for each in response.doc('#J_list li h4>a').items():
            name = each.text()
            save= {"name": name, "type_name": 'collection'}
            self.crawl(each.attr.href, callback=self.list_page, save=save)

        for list_link in response.doc('.ui-page-inner a').items():
            list_href = pq(list_link).attr.href
            if list_href is not None and len(list_href)>0 :
                self.crawl(list_href, callback=self.collection_list)

    @config(age=24*60 * 3)
    def material_page(self, response):
        for each in response.doc('.category_sub2 a').items():
            name = each.text()
            save= {"name": name, "type_name": 'material'}
            self.crawl(each.attr.href, callback=self.list_page, save=save)

