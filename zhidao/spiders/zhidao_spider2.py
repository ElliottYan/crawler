import scrapy
import os
import io
import sys
import pdb

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

class zhidao_spider(scrapy.Spider):
    name = 'zhidao_spider'

    count = 0

    start_urls = [
        "https://zhidao.baidu.com/search?word=%CE%AA%CA%B2%C3%B4&ie=gbk&site=-1&sites=0&date=0&pn=0"
        # 'https://zhidao.baidu.com/question/43237748.html?fr=iks&word=%CC%EC%CE%AA%CA%B2%C3%B4%BB%E1%CF%C2%D3%EA&ie=gbk'
    ]
    

    def parse_question_page(self, response):
        saving_path = './data/'
        body = response.css('div#body')
        title = body.css('span.ask-title::text').extract_first()
        if title is None:
            return

        # here best answer text is a list
        best_answer = body.css('div[id*="best-content"]')
        best_answer_texts = best_answer.css('p::text').extract()
        best_answer_texts = ' '.join(best_answer_texts)

        # list of pic urls
        best_answer_pics = ','.join(best_answer.css('p a img::attr(src)').extract())

        # list of related questions
        related_questions = body.css('div li span[class*="related"]::text').extract()

        with open(os.path.join(saving_path, 'title-{}.txt'.format(title)), 'wb') as f:
            f.write('Q: \n{}'.format(title+'\n').encode('utf-8'))
            f.write('A:\n {}'.format(best_answer_texts+'\n').encode('utf-8'))
            f.write('pics:\n {}'.format(best_answer_pics+'\n').encode('utf-8'))
            f.write('Related Q:\n'.encode('utf-8'))
            f.write('\n'.join(related_questions).encode('utf-8'))

    def parse(self, response):
        # pdb.set_trace()
        zhidao_spider.count += 1
        if zhidao_spider.count > 2:
            return
        body = response.css('div#body')
        href_lists = body.css('div.list-inner div.list dl dt a::attr(href)').extract()
        for item in href_lists:
            yield scrapy.Request(item, callback=self.parse_question_page)

        next_page = body.css('div.pager a.pager-next::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
        return

