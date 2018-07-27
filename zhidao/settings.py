# -*- coding: utf-8 -*-

# Scrapy settings for zhidao project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

# from fake_useragent import UserAgent


# ua = UserAgent()
# USER_AGENT = ua.random
DOWNLOAD_DELAY = 0.5

BOT_NAME = 'zhidao'

SPIDER_MODULES = ['zhidao.spiders']
NEWSPIDER_MODULE = 'zhidao.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhidao (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'zhidao.rotate_useragent.RotateUserAgentMiddleware' :400
    }


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
# MEMUSAGE_LIMIT_MB = 2048

COOKIE = '_dacevid3=d7af0fb3.c84c.ae6a.eca3.aeccccfeb8d7; __gads=ID=0a14d0a492c9cc95:T=1530594981:S=ALNI_MYgqdXgqO-F1MyeTAiKOw7Lx6OPyg; _HUPUSSOID=69f43b93-e5a0-4581-9f28-84afcd7653c5; UM_distinctid=1647d9d0c720-0b05e24f48c918-5b163f13-144000-1647d9d0c73e4; Hm_lvt_3d37bd93521c56eba4cc11e2353632e2=1531115802; PHPSESSID=b921ed335cad248fcbc3effdd4d706a9; _cnzz_CV30020080=buzi_cookie%7Cd7af0fb3.c84c.ae6a.eca3.aeccccfeb8d7%7C-1; _fmdata=bxwwcqI0OkfClrP5IJdzHJRCnqRQBkrLfNjI5I68GXW12MGoEioezEUma8VrPYewrVe%2BDU71GIhvTDXYBU05jv4xmejd3penpqtDPb%2Bmd%2B8%3D; _CLT=00376064be821b71351c003dda774e37; u=25333842|RWxsaW90dDM3|4e79|748bab7548cb06b75f00e1ae52fe2d9f|48cb06b75f00e1ae|aHVwdV8wNDU4ZmYxNWYwY2UzYTI5; us=a5969167e502c7efa9ebf38a383fe4062863426b7e02418f81e6152539fee4bc2ceefe78f66baab84ca3ce982f17fbb713f9fd492311a0f94829b2d2a83d923e; ua=35609044; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1531188967,1531188972,1531193424,1531193425; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1531193425; __dacevst=122fecb5.9a2b7e56|1531195227746'


# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhidao.middlewares.ZhidaoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhidao.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'zhidao.pipelines.ZhidaoPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#settings.py文件
# DOWNLOADER_MIDDLEWARES = {
#   'Lagou.middlewares.RandomUserAgentMiddleware': 543,
#   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None, #这里要设置原来的scrapy的useragent为None，否者会被覆盖掉
#}
# RANDOM_UA_TYPE='random'