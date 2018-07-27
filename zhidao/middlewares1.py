#middlewares.py文件
from fake_useragent import UserAgent #这是一个随机UserAgent的包，里面有很多UserAgent
class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random') #从setting文件中读取RANDOM_UA_TYPE值

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)

        user_agent_random=get_ua()
        request.headers.setdefault('User-Agent', user_agent_random) #这样就是实现了User-Agent的随即变换