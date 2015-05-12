#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-05-12 13:34:11
# Project: meishi_material

from pyspider.libs.base_handler import *
from pyquery import PyQuery as pq

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=10)
    def on_start(self):
        self.crawl('http://www.meishichina.com/YuanLiao/', callback=self.list_page)

    @config(age=10)
    def list_page(self, response):
        for each in response.doc('.category_sub1').items():
            material_type = each.text()
            for link in pq(each).siblings('.category_sub2>a[target="_blank"]').items():
                raw_href = link.attr.href
                if raw_href[-1] == '/':
                    use_href = raw_href + 'useful/'
                else:
                    use_href = raw_href + '/useful/'
                self.crawl(use_href, callback=self.detail_page, save={"material_type": material_type})

    @config(priority=2)
    def detail_page(self, response):
        material_type = response.save['material_type']
        name = response.doc('h2#category_title').text()
        pic = response.doc('#category_pic').attr["data-src"]
        intro = response.doc('#category_txt1').text()
        nutrition = []
        for each in response.doc('.category_use_table li>div').items():
            quantanty = pq(each).find('span').text()
            nutrition_name = pq(each).remove('span').text()
            nut = {
                nutrition_name : quantanty
            }
            nutrition.append(nut)
        description = response.doc('.category_usebox').html()

        return {
            "name": name,
            "cover": pic,
            "intro":  intro,
            "nutrition": nutrition,
            "description": description,
            "material_type": material_type
        }
