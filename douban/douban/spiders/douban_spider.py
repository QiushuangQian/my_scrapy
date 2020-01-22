# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'douban_spider'
    # 允许域名
    allowed_domains = ['movie.douban.com']
    # 入口，扔到调度器里
    start_urls = ['http://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        # 循环电影条目
        for i_item in movie_list:
            # 导入item文件
            douban_item = DoubanItem()
            # 写详细的xpath，进行数据解析
            # /text() 以文本形式输出    extract()抽取
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(
                ".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = i_item.xpath(".//div[@class='bd']//div[@class='star']/span[2]/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(
                ".//div[@class='bd']//div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//div[@class='bd']//p[@class='quote']/span[@class='inq']/text()").extract_first()
            # 必须将数据yield到pipline中
            yield douban_item
        # 下一页请求，取后一页xpath
        next_link = response.xpath(".//div[@class='paginator']/span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)
