from unicodedata import name
from itsdangerous import json
import scrapy
from send.items import ShopItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from json import loads

class TvSpider(scrapy.Spider):
    name = 'tv'
    start_urls = ['https://ek.ua/ua/list/160/']
    token=""

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url = url, 
                callback = self.parse,
                wait_time = 100,
                wait_until = EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.model-all-shops'))
            )

    def parse(self, response):
        for goods in response.css("table.model-short-block"):
            price_tables = goods.css('table.model-short-block tr')
            for shop in price_tables:
                yield ShopItem(
                    name = shop.xpath('.//td[@class="model-hot-prices-td"]//a//u/text()').get(),
                    price = shop.xpath('.//td[@class="model-shop-price"]//a/text()').get()
                )

    def after_post(self, response):
        pass

    def save_token(self, response):
        token = loads(response.body).get("token")
        self.logger.critical(f"Get tocken {token}")
        self.token = token