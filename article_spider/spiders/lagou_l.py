# -*- coding: utf-8 -*-
import scrapy
import json

class LagouLSpider(scrapy.Spider):

    name = 'lagou_l'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    headers = {
        "HOST": "www.lagou.com",
        "Referer": "https://www.lagou.com",
        'User-Agent': agent
    }

    def parse(self, response):
        pass


    def start_requests(self):

        return [scrapy.Request(
            'https://www.lagou.com',
            headers=self.headers,
            callback=self.login)]

    def login(self,response):
        post_url = "https://www.lagou.com/login/login.json"
        post_data = {
            "phone_num": '18227587882',
            "password": 'cw7340117',
        }

        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self,response):

        print (response.text)

