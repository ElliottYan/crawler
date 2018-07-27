import scrapy
import os
import io
import sys
import pdb
import scrapy
import io
import sys
import locale

reload(sys)
sys.setdefaultencoding('utf-8')

# locale.setlocale(locale.LC_ALL, str('en_US.UTF-8'))


class tom61(scrapy.Spider):
    name = 'tom61_spider'
    start_urls = [
        'http://m.tom61.com/index.php?bclassid=400',
        'http://m.tom61.com/index.php?bclassid=106',
        'http://m.tom61.com/index.php?bclassid=33',
        'http://m.tom61.com/index.php?bclassid=685',
        'http://m.tom61.com/index.php?bclassid=257'
    ]

    # saving_path = 'e:\coding\crawler\zhidao\data'
    saving_path = u'./data/'

    def parse(self, response):
        # extract title
        body = response.css('li')
        parse_type = bool(body.css('.blc_1'))

        if parse_type:
            title = unicode(response.css('head title::text').extract_first().split('-')[0])

            if 'dir' in response.meta.keys():
               saving_dir = response.meta['dir']
            else:
                saving_dir = tom61.saving_path
            saving_dir = os.path.join(saving_dir, title).encode('utf-8')
            if not os.path.exists(saving_dir):
                os.mkdir(saving_dir)
            body = response.css('li')
            hrefs = body.css('a::attr(href)').extract()
            types = body.css('a::text').extract()
            parse_func = self.parse

            tag = response.meta['tag'] + '#' + title if 'tag' in response.meta.keys() else title

            # parse_func = self.parse

            type_href = list(zip(types, hrefs))
            for type, href in type_href:
                href = response.urljoin(href)
                request = scrapy.Request(href, callback=self.parse)
                request.meta['dir'] = saving_dir
                request.meta['tag'] = tag
                yield request

        else:
            title = unicode(response.css('head title::text').extract_first().split('-')[0])
            if 'dir' in response.meta.keys():
                saving_dir = response.meta['dir']
            else:
                saving_dir = tom61.saving_path
            saving_dir = os.path.join(saving_dir, title).encode('utf-8')
            if not os.path.exists(saving_dir):
                os.mkdir(saving_dir)

            hrefs = response.css('li a::attr(href)').extract()

            for item in hrefs:
                item = response.urljoin(item)
                request = scrapy.Request(item, callback=self.parse_page)
                request.meta['dir'] = saving_dir
                request.meta['tag'] = response.meta['tag'] + '#' + title
                yield request

            next_page = response.css('div.next a::attr(href)').extract_first()
            if next_page:
                next_page = response.urljoin(next_page)
                request = scrapy.Request(next_page, callback=self.parse)
                request.meta['dir'] = response.meta['dir']
                request.meta['tag'] = response.meta['tag']
                yield request

    def parse_page(self, response):
        body = response.css('div.detail')
        if not body:
            return
        title = unicode(body.css('h1::text').extract_first().split('-')[0])
        text = unicode(("\n".join(body.css('p::text').extract())))
        tag = unicode(u'#' + response.meta['tag'])
        saving_dir = response.meta['dir']
        saving_path = os.path.join(saving_dir, (title + '.txt').encode('utf-8'))
        length = len(text)
        with open(saving_path, 'wb') as f:
            f.write(u"\n".join([tag, unicode(length), text]))
        # pdb.set_trace()




