# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from wsgiref import headers
from scrapy import signals
from scrapy.http import JsonRequest
from scrapy.utils.serialize import ScrapyJSONEncoder
from send.items import ShopItem
from json import dumps
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class SendSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # робимо копію методу декодування ScrapyItem до JSON
    encode = ScrapyJSONEncoder().encode
    def process_spider_output(self, response, result, spider):
        for i in result:
            if isinstance(i, ShopItem): #якщо павук повернув результат потрібного типу
                yield JsonRequest( # надсилаємо JSON POST запит
                    url="https://localhost:44375/api/Shops/", #на адресу сервера,
                    method="POST",
                    headers={
                        "Authorization":f"Bearer {spider.token}"
                    },
                    body=self.encode(i), # в тіло запиту записуємо декодовну item
                    callback=spider.after_post # вказуєм обробник відповіді. Якщо нічого не вказати то обробку передасть в spider.parse
                )
            yield i

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.        
        # Must return only requests (not items).
        yield JsonRequest( # надсилаємо JSON POST запит
                url="https://localhost:44375/api/users/login", #на адресу сервера,
                method="POST",
                body=dumps({
                    "Login":"Login",
                    "Password":"Password"
                }),
                callback=spider.save_token # вказуєм обробник відповіді. Якщо нічого не вказати то обробку передасть в spider.parse
            )

        for r in start_requests:
            yield r
        
  
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SendDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
