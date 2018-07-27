import sys
import pdb
import scrapy
import io

class tom(scrapy.Spider):
    name = 'tom_spider'
    start_urls = [
        'http://m.tom61.com/index.php?bclassid=400',
        'http://m.tom61.com/index.php?bclassid=106',
        'http://m.tom61.com/index.php?bclassid=33',
        'http://m.tom61.com/index.php?bclassid=685',
        'http://m.tom61.com/index.php?bclassid=257'
    ]