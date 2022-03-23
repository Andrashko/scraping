from gc import callbacks
from urllib.request import Request
import scrapy
import logging
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from dinamyc.items import DinamycItem

class InstagramSpider(scrapy.Spider):
    name = "instagram"
    start_urls = ["https://www.instagram.com/"]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=1000,
                wait_until=expected_conditions.element_to_be_clickable(
                   ( By.CSS_SELECTOR,
                    ".aaa li button")
                )                
            )

    def parse(self, response, **kwargs):
        for img in response.css("li img"):
            yield DinamycItem(url=img.css('::attr(src)').get())
    