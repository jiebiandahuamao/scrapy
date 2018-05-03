# -*- coding: utf-8 -*-
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(['scrapy','crawl','jobble'])
#execute(['scrapy','crawl','lagou'])
# execute(['scrapy','crawl','lagou_l'])
execute(['scrapy','crawl','lagou2'])