#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import os
import io, re
import sys
import pdb
import urllib
import codecs
from scrapy.xlib.pydispatch import dispatcher

def create_requested_urls(template_url, f_path):
    singer_set = set()
    with codecs.open(f_path, 'r', 'utf-8') as f:
        lines = f.readlines()
    for line in lines:
        singer_set.add(line.strip())
    ret_urls = []
    for item in singer_set:
        ret_urls.append(os.path.join(template_url, urllib.quote(item.encode('utf-8'))))
    print("ret url length: {}".format(str(len(ret_urls))))
    return ret_urls


class baike_spider(scrapy.Spider):
    name = 'baike_spider'
    
    saving_path = './data/baike'
    # start_urls = create_requested_urls(template_url, f_path)
    start_urls = ['http://www.baike.com/wiki/%E9%83%AD%E9%87%87%E6%B4%81']
    cursor = 0
    
    def create_urls(self, limit):
        f_path = "./data/extracted_singer_set_1000.txt"
        template_url = "http://www.baike.com/wiki/"
        urls = create_requested_urls(template_url, f_path)
        
        ret = urls[baike_spider.cursor:baike_spider.cursor+limit]
        baike_spider.cursor += limit
        return ret
    #
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse_page)

    def __init__(self, *args, **kwargs):
        super(baike_spider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.queue_more_requests, scrapy.signals.spider_idle)
        
    def queue_more_requests(self, spider):
        urls = self.create_urls(1000)
        
        if not urls:
            return
        
        for url in urls:
            req = self.make_requests_from_url(url)
            self.crawler.engine.crawl(req, spider)
            

    def parse(self, response):
        title_block = response.css('div#primary div.content-h1 h1')
        # skip when entering the search block
        if not title_block:
            return
        
        title = title_block.css('::text').extract_first()
        
        relation = response.css('div#figurerelation ul li')
        
        celebrity_rel = []
        celebrity_name = []
        
        for item in relation:
            celebrity_name.append("".join(item.css('a::text').extract()).strip())
            # lots of '\n' inside
            celebrity_rel.append("".join(item.xpath('./text()').extract()).strip())
        assert len(celebrity_rel) == len(celebrity_name)
        rel_text = '\n'.join([celebrity_name[ix] + '\t' + celebrity_rel[ix] for ix in range(len(celebrity_name))])

        summary = response.css('div#primary div.information > div.summary > p').xpath('.//text()').extract()
        
        # basic infos
        infos = response.css('div#primary div#datamodule div[class="module zoom"]')
        info_texts = []
        if infos:
            infos = infos[0].css('table td')
        else:
            for item in infos:
                # consisting some empty tds
                if not item.css('strong'):
                    continue
                info_texts.append(''.join(map(unicode.strip, item.xpath('.//text()').extract())))
        
        # pdb.set_trace()
        prize_title = response.css('div.content_h2 h2')
        prize_item = None
        for item in prize_title :
            if "".join(item.css('::text').extract()).strip().startswith('获奖'):
                prize_item = item
        prize_text = ''
        if prize_item:
            # todo: this fails if empty table exists...
            table = prize_item.xpath('./following::table')[0]
            # there are many \xa0 as delimiters
            prize_text = "\n".join(map(unicode.strip, table.xpath('.//text()').extract()))
            prize_text = re.sub(r'\xa0', '\t', prize_text)


        # fname = title.encode('utf-8') + '.txt'
        fname = os.path.basename(response.url)
        with open(os.path.join(baike_spider.saving_path, fname), 'wb') as f:
            f.write('title:\n{}\n\n'.format(title + '\n').encode('utf-8'))
            f.write('intros:\n{}\n\n'.format(' '.join(summary)+'\n').encode('utf-8'))
            if info_texts:
                f.write('basic infos:\n{}\n\n'.format('\n'.join(info_texts)).encode('utf-8'))
            if rel_text:
                f.write('relations:\n{}\n\n'.format(rel_text).encode('utf-8'))
            if prize_text:
                f.write('prize:\n{}\n\n'.format(prize_text).encode('utf-8'))
        return
