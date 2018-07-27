import scrapy
import os
import io
import sys
import pdb


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def read_in_urls(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    urls = [line.strip() for line in lines]
    return urls


class zhidao_spider(scrapy.Spider):
    name = 'zhidao_spider3'
    
    count = 0
    
    file_path = 'E:/coding/crawler/tmp/baiduurl.txt'
    
    start_urls = read_in_urls(file_path)
    
    def parse(self, response):
        saving_path = './data/zhidao'
        body = response.css('div#body')
        title = body.css('span.ask-title::text').extract_first()
        if title is None:
            return
        
        q_content = " ".join(body.css('div[class="line mt-5 q-content"] span::text').extract())
        
        # here best answer text is a list
        best_answer = body.css('div[id*="best-content"]')
        best_answer_texts = best_answer.css('p::text').extract()
        best_answer_texts = ' '.join(best_answer_texts)
        
        # list of pic urls
        best_answer_pics = ','.join(best_answer.css('p a img::attr(src)').extract())
        
        # list of related questions
        related_questions = body.css('div li span[class*="related"]::text').extract()
        name = os.path.basename(response.url).split('?')[0].split(".")[0]
        fname = "{}.txt".format(name)
        if os.path.exists(os.path.join(saving_path, fname)):
            return
        with open(os.path.join(saving_path, fname), 'wb') as f:
            f.write('Q:\n{}'.format(title + '\n').encode('utf-8'))
            f.write('Q_content:\n{}'.format(q_content+'\n').encode('utf-8'))
            f.write('A:\n {}'.format(best_answer_texts + '\n').encode('utf-8'))
            f.write('pics:\n {}'.format(best_answer_pics + '\n').encode('utf-8'))
            f.write('Related Q:\n'.encode('utf-8'))
            f.write('\n'.join(related_questions).encode('utf-8'))
        
        next_pages = body.css('a::attr(href)').extract()
        for next_page_url in next_pages:
            if next_page_url.split('/')[1] != 'question':
                continue
            else:
                request = scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
                yield request
         

