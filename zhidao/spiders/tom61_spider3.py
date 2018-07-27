# coding=utf-8

import scrapy
import os
import io
import sys
import pdb
import scrapy
import io
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class tom61_spider3(scrapy.Spider):
    name = 'tom61_spider3'
    start_urls = ['http://www.tom61.com/chengyudaquan/index.html']
    DATA_ROOT = 'D:\work files\data\成语大全'

    def parse(self, response):
        list = response.css('div[class="t_auto pb16"]#Mhead2_0 dd a')
        urls = list.css('::attr(href)').extract()
        titles = list.css('::attr(title)').extract()
        for ix, url in enumerate(urls):
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta['title'] = titles[ix]
            yield request
        next_page = response.css('div.t_fy span + a').css('::attr(href)').extract_first()
        if next_page:
            request = scrapy.Request(response.urljoin(next_page), callback=self.parse)
            yield request

    def parse_page(self, response):
        title = response.meta['title']
        text = "\n".join(response.css('div.t_news::text').extract()).strip()
        with open(os.path.join(tom61_spider3.DATA_ROOT, title + '.txt'), 'w') as f:
            f.write(text)
        return



