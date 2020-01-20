# -*- coding: utf-8 -*-
import scrapy


class DoubanSpiderSpider(scrapy.Spider):
    #爬虫名
    name = 'douban_spider'
    #允许域名
    allowed_domains = ['movie.douban.com']
    #入口，扔到调度器里
    start_urls = ['http://movie.douban.com/top250']

    #解析
    def parse(self, response):
        print(response.text)
