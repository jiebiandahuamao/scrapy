# -*- coding: utf-8 -*-
"""
cw
"""
import requests
from scrapy.selector import Selector
import pymysql

db = pymysql.connect(host = "localhost",user = "root",passwd = "shutdown",db = "spider",charset="utf8")
cursor = db.cursor()


def crawl_ips():
    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}
    for i in range(100):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i),headers = headers)

    selector = Selector(text = re.text)
    all_trs = selector.css("#ip_list tr")[1:]

    ip_list = []
    for tr in all_trs:
        speed_str = tr.css(".bar::attr(title)").extract()[0]

        if speed_str:
            speed = float(speed_str.split("秒")[0])
        all_texts = tr.css("td::text").extract()

        ip = all_texts[0]
        port = all_texts[1]
        proxy_type = all_texts[5]

        ip_list.append((ip,port,proxy_type,speed))

    for ip_info in ip_list:
        try:
            cursor.execute(
                "insert proxy_ip(ip,port,speed,proxy_type) VALUES ('{0}','{1}','{2}','{3}')".format(
                    ip_info[0],ip_info[1],ip_info[3],ip_info[2]
                )
            )
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

class Get_ip(object):

    def delete_ip(self,ip):
        delete_sql = """delete from proxy_ip where ip = '{0}'""".format(ip)
        cursor.execute(delete_sql)
        db.commit()
        return True

    def judge_ip(self,ip,port):
        http_url = 'http://www.baidu.com'
        proxy_url = 'http://{0}:{1}'.format(ip,port)
        try:

            proxy_dict = {
                "http":proxy_url
            }
            requests.get(http_url,proxies=proxy_dict)
            return True
        except Exception as e:
            print(e)
            print ("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code <=200 and code >= 300:
                print ("effective ip")
                return True
            else:
                print("invalid ip")
                self.delete(ip)
                return False

    def get_random_ip(self):
        sql = """select ip,port from proxy_ip order by rand() limit 1"""
        result = cursor.execute(sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip,port)
            if judge_re:
                return "http://{0}:{1}".format(ip,port)
            else:
                return self.get_random_ip()

crawl_ips()
# get_ip= Get_ip()
# print(get_ip.get_random_ip())