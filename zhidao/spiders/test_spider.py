
import scrapy

class test(scrapy.Spider):

    name = "test"

    start_urls = ['http://lab.scrapyd.cn']
    saving_dir = 'data\\'

    def parse(self, response):
        page = response.url.split("/")[-2]
        tmp = response.css('div.quote')
        for item in tmp:
            text = item.css('.text::text').extract_first()
            author = item.css('.author::text').extract_first()
            tag = item.css('.tag::text').extract()
            tag = ','.join(tag)
            file_name = 'quote-{}.txt'.format(author)
            with open(file_name, 'w') as f:
                f.write(text)
                f.write('\n')
                f.write('tag: {}'.format(tag))
            self.log('saving: {}'.format(file_name))

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)