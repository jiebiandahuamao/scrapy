# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from selenium import webdriver
import re
from scrapy.loader import ItemLoader
from article_spider.items import LagouJobItem, LagouJobItemLoader

browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
browser.get("https://passport.lagou.com/login/login.html")

browser.find_element_by_css_selector(".form_body input[type='text'] ").send_keys("18227587882")
browser.find_element_by_css_selector(".form_body input[type='password'] ").send_keys("cw7340117")
browser.find_element_by_css_selector(".form_body input[type='submit']").click()

class Lagou2Spider(scrapy.Spider):
    name = 'lagou2'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    headers = {
        "HOST": "www.lagou.com",
        "Referer": "https://www.lagou.com",
        'User-Agent': agent
    }

    def parse(self, response):

        t_selector = Selector(text=browser.page_source)
        all= t_selector.css("a::attr(href)").extract()
        all_urls = filter(lambda x: True if x.startswith("https") else False, all)
        for url in all_urls:
            match_obj = re.match("(.*www.lagou.com/(zhaopin|jobs)/).*", url)
            if match_obj:
                request_url = match_obj.group()
                yield scrapy.Request(request_url, headers=self.headers, callback=self.do_items)

            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)


    def do_items(self,response):
        print (response)
        print (111)
        item_loader = ItemLoader(item=LagouJobItem(),response=response)
        item_loader.add_css("title", ".job-name span::text")
        item_loader.add_value("url", response.url)
        item_loader.add_css("salary", ".salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")

        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_css("company_name", "#job_company dt a div h2::text")

        job_item = item_loader.load_item()
        print (job_item)
        return job_item
