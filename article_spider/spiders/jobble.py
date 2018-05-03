# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # 获取所有的url
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            #Request(url=post_url,callback=self.parse_detail)   方式一(能取到完整域名额情况下)
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse_detail)
        #提取下一页
        next_urls = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_urls:
            yield Request(url=parse.urljoin(response.url,next_urls),callback=self.parse)


    def parse_detail(self, response):
        #解析具体文章的逻辑
        re_select = response.xpath("//*[@id='post-113740']/div[1]/h1/text()")
        print(re_select)

