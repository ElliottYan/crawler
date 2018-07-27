import scrapy
import os
import io
import sys
import pdb
import scrapy
import io
import sys
import locale
import re
from scrapy.conf import settings

reload(sys)
sys.setdefaultencoding('utf-8')

class hupu_spider(scrapy.Spider):
    name = 'hupu_spider'

    start_urls = ['https://bbs.hupu.com/vote-2',
                  'https://bbs.hupu.com/bxj-2',
                  'https://bbs.hupu.com/topic-2']

    DATA_ROOT = './data/hupu/'

    # parse function for list pages
    def parse(self, response):
        lists = response.css('form#ajaxtable ul > li > div.titlelink > a')
        urls = lists.css('::attr(href)').extract()

        tmp = response.url.split('-')
        try:
            next_page = tmp[0] + '-' + str(int(tmp[1]) + 1)
            print("next_page:\n {}".format(next_page))
        except:
            return

        for url in urls:
            request = scrapy.Request(response.urljoin(url), callback=self.parse_page, cookies=stringToDict(settings['COOKIE']))
            yield request

        request_next_page = scrapy.Request(response.urljoin(next_page), callback=self.parse, cookies=stringToDict(settings['COOKIE']))
        yield request_next_page
        print(response.urljoin(url))

    def parse_page(self, response):
        filename = response.meta['filename'] if 'filename' in response.meta.keys() \
                                            else os.path.basename(response.url)
        ret = []
        floors = response.css('div#t_main > form > div.floor div.floor_box')
        title = response.css('head > title::text').extract_first().split('-')[0]
        # deals with hyper-links

        def parse_box(floor, response):
            id = each_floor.css('div.author > div.right > a[id]').xpath('@id').extract_first()
            if not id:
                print('Fails.')
                return None, None, None
            # extract quote_ref_id
            if not id:
                quote_ref_id = str(-1)
            else:
                quote = floor.css('table.case tr td').css('blockquote > p > b::text').extract_first()
                quote_ref_id = re.findall(r'\d+', quote)[0] if quote else 0

            floor = floor.css('table tr td')
            if id == u'0':
                floor = floor.css('div.quote-content')
                img = floor.css('img')
                skip = bool(img)
                if skip:
                    return id, quote_ref_id, ""

            # paras = floor.css('p')

            # if not paras:
            #     text_0 = "\n".join(floor.css('::text').extract())
            #     href_texts = floor.css('a[target="_brank"]::text').extract()
            #     if href_texts:
            #         try:
            #             findall = re.findall(r'<a.*?>.*?</a>', text_0)
            #         except:
            #             pdb.set_trace()
            #         try:
            #             assert len(findall) == len(href_texts)
            #         except:
            #             pdb.set_trace()
            #         for j, href_text in enumerate(href_texts):
            #             text_0 = re.sub(findall[j], href_text, text_0)

            text_0 = ("\n".join(floor.xpath('./text() | '
                                            './div/text() | '
                                            './p/text() | '
                                            './a/text() | '
                                            './p/*[not(local-name()="small")]/text() | '
                                            './span/text() | '
                                            './span/*[not(local-name()="small")]/text()').extract())).strip()

            return id, quote_ref_id, text_0

            # ret = []
            # for ix, item in enumerate(paras):
            #     # remove <p> and </p>
            #     # pdb.set_trace()
            #     try:
            #         line_text = item.extract()[3:-4]
            #     except:
            #         pdb.set_trace()
            #     href_texts = item.css('a[target="_brank"]::text').extract()
            #     # remove hyper-links with texts
            #     if href_texts:
            #         findall = re.findall(r'<a.*?>.*?</a>', line_text)
            #         assert len(findall) == len(href_texts)
            #         for j, href_text in enumerate(href_texts):
            #             line_text = re.sub(findall[j], href_text, line_text).strip()
            #             ret.append(line_text)
            # return id, quote_ref_id, '\n'.join(ret).strip()

        # write in title
        # maybe the file is already existed
        file_path = os.path.join(hupu_spider.DATA_ROOT, filename + '.txt')
        if not os.path.exists(file_path):
            with open(os.path.join(hupu_spider.DATA_ROOT, filename + '.txt'), 'ab') as f:
                f.write(unicode(title))
                f.write('\n\n')

        # write in the floor texts
        for each_floor in floors:
            ret = parse_box(each_floor, response)
            # pdb.set_trace()
            with open(os.path.join(hupu_spider.DATA_ROOT, filename + '.txt'), 'ab') as f:
                f.write(u'\n'.join([unicode(item) for item in ret]))
                f.write(u'\n\n')

        next_page = response.css('div#t_main > div[class="page downpage"] > a')

        # generate next_page request
        next_page_url = get_next_page_url(response.url)
        request = scrapy.Request(next_page_url, callback=self.parse_page, cookies=stringToDict(settings['COOKIE']))
        request.meta['filename'] = filename
        yield request

        return

def get_next_page_url(url):
    url = url.split('/')

    split_postfix = url[-1].split('.')
    tmp = split_postfix[0].split('-')
    # assume the length of tmp should be 2
    postfix = split_postfix[1] if len(split_postfix) == 2 else ""
    if len(tmp) != 2:
        new_url = '.'.join([tmp[0] + '-1', postfix])
        new_url = '/'.join(url[:-1] + [new_url])
        return get_next_page_url(new_url)

    url_without_postfix = "-".join([tmp[0], str(int(tmp[-1]) + 1)])
    next_page_url = ".".join([url_without_postfix, postfix])
    next_page_url = "/".join(url[:-1] + [next_page_url])
    return next_page_url



def stringToDict(cookie):
    itemDict  = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict

if __name__  == '__main__':
    while True:
        input = raw_input("Please input the url:\n")
        print(get_next_page_url(input))


