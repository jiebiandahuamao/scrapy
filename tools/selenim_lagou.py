#-*- coding:utf8 -*-

"""
author:cw
通过selenium 模拟登录拉钩
"""

from selenium import webdriver

browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver")

browser.get("https://passport.lagou.com/login/login.html")

browser.find_element_by_css_selector(".form_body input[type='text'] ").send_keys("18227587882")
browser.find_element_by_css_selector(".form_body input[type='password'] ").send_keys("cw7340117")
browser.find_element_by_css_selector(".form_body input[type='submit']").click()



# browser.quit()