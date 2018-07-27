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


class Hundred_thousand(scrapy.Spider):
    name = 'ht_spider'
    start_urls = [
      'http://www.100000whys.com/'
    ]

    saving_path = './data'

    # parse_function for index page
    def parse(self, response):
        hrefs = response.css('div#d ul.nav > li > a::attr(href)').extract()[1:]

        for url in hrefs:
            request = scrapy.Request(url, callback=self.parse_list)
            yield request

    def parse_list(self, response):
        title = response.css('head title::text').extract_first()
        hrefs = response.css('div#j div#f h2 > a::attr(href)').extract()
        for url in hrefs:
            url = response.urljoin(url)
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta['saving_path'] = os.path.join(Hundred_thousand.saving_path, title + '.txt')

        next_page = response.css('div#j > div#f div.navigation div.pagination > span + a').extract_first()
        if next_page:
            request_next_page = scrapy.Request(next_page)
            yield request_next_page

    def parse_page(self, response):
        tags = u"#".join(response.css('div.n span a::text').extract())
        # save title and text
        body = response.css('div.n_n')
        title = body.css('h1::text').extract_first()
        text = u"\n".join(body.css('p:text').extract())

        with open(response.meta['saving_path'], 'ab') as f:
            f.write(u'\t'.join[title, text, tags])
            f.write('\n\n')



