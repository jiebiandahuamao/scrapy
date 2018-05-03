# -*- coding: utf-8 -*-

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
headers = {
    "HOST": "www.lagou.com",
    "Referrer": "https://www.lagou.com",
    'User-Agent': agent
}

def lagou_login(account,password):

    post_url = "https://www.lagou.com/login/login.json"

    post_data = {
        "phone_num":account,
        "password":password,
    }
    response_text = session.post(post_url,data=post_data,headers=headers)

    session.cookies.save()

lagou_login('18227587882','cw7340117')