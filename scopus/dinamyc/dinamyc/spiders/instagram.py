from gc import callbacks
from http import cookies
from urllib.request import Request
from wsgiref import headers
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
              
                ),            
                cookies={
                    'mid':'Yjq4AAALAAF6ZoawuT6NHIlQt9FY',
                    "ig_did":"A8FD8FA0-EFDC-4165-8077-CA8984F63E33",
                    "ig_nrcb":"1",
                    "csrftoken":"gurWK64PvHRtkVxjJIY6YkyKB7jNyFbj",
                    "ds_user_id":"11817601325",
                    "sessionid":"11817601325%3Aqb6WMltkdmjvx6%3A10",
                    "dpr":"1.25",
                    "rur":"LDC\\05411817601325\\0541679552309:01f7f1cf5a3fa2e6b1f7ae21fe10413c951be85dfebefc2e42098a92be2512417975092d"
                }
            )

    def parse(self, response, **kwargs):
        for img in response.css("li img"):
            yield DinamycItem(url=img.css('::attr(src)').get())
    