# -*- coding: utf-8 -*-
import scrapy
import json


class ApiVcBilibiliSpider(scrapy.Spider):
    name = 'api.vc.bilibili'
    allowed_domains = ['api.vc.bilibili.com']
    start_urls = [
        'https://api.vc.bilibili.com/link_draw/v2/Photo/list?category=sifu&type=new&page_num={}&page_size=20'.format(i)
        for i in range(426)]

    def parse(self, response):
        for i in json.loads(response.text)['data']['items']:
            yield {'image_urls': (picture['img_src'] for picture in i['item']['pictures'])}
