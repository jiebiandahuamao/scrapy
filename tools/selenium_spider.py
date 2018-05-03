# -*- coding:utf8 -*-
"""
通过selenium爬取动态数据(京东价格)
"""
from selenium import webdriver
#scrapy 的selector 速度快些,虽然selenium也支持css等的选择,但是selenium是纯python写的,会慢些
from scrapy import Selector

browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver")

browser.get("https://item.jd.com/11878958311.html")
print(browser.page_source)

t_selector = Selector(text = browser.page_source)
a = t_selector.css(".p-price .price::text").extract()
print (a)
browser.quit()